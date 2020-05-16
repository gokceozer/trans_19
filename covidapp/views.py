from django.shortcuts import render, get_object_or_404
from covidapp.forms import PatientForm, QueryForm, LocationForm, PastLocationForm #LocationFormSet
from covidapp.models import Patient, Location, LocationTemplate
from django.views.generic import DetailView, ListView, FormView, UpdateView, DeleteView
from . import forms
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
import datetime
from collections import OrderedDict
from django.urls import reverse_lazy, reverse

# Create your views here.
def index(request):
    patient_dict = Patient.objects.order_by('case_number')
    my_dict = {'patients':patient_dict}
    return render(request, 'covidapp/index.html',context=my_dict)


def patient_new(request):
    patientForm = PatientForm()
    if request.method == "POST":
        patientForm = PatientForm(request.POST)
        if patientForm.is_valid(): #and formset.is_valid():
            patientForm.save(commit=True)
            return index(request)
        else:
            print('ERROR FORM INVALID')
    return render(request, 'covidapp/patient_new.html',{'patientForm':patientForm})


def location_new(request):
    locationForm = LocationForm()
    if request.method == "POST":

        loc = LocationForm(request.POST) 
        if loc.is_valid():
            loc.save(commit=True)

            return index(request)
        else:
            print('ERROR FORM INVALID')

    return render(request, 'covidapp/location_new.html',{'locationForm':locationForm})

class PatientDetailView(DetailView, FormMixin):
    model=Patient
    form_class = PastLocationForm
    #template_name = 'patient_detail.html'

    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        
        form = self.get_form()

        if form.is_valid():
            pastLocationDetail = Location()

            setattr(pastLocationDetail,'location_name',str(form.cleaned_data['location']).split(',')[0])
            setattr(pastLocationDetail,'address',str(form.cleaned_data['location']).split(',')[1].split(', ')[0])
            setattr(pastLocationDetail,'district',str(form.cleaned_data['location']).split('District: ')[1].split(',')[0])
            setattr(pastLocationDetail,'grid_x',int(str(form.cleaned_data['location']).split('Coordinates: (')[1].split(', ')[0]))
            setattr(pastLocationDetail,'grid_y',int(str(form.cleaned_data['location']).split('Coordinates: (')[1].split(', ')[1][:-1]))
            setattr(pastLocationDetail,'date_from',form.cleaned_data['date_from'])
            setattr(pastLocationDetail,'date_to',form.cleaned_data['date_to'])
            setattr(pastLocationDetail,'details',form.cleaned_data['details'])
            setattr(pastLocationDetail,'category',form.cleaned_data['category'])
            setattr(pastLocationDetail,'patient', self.object)


            pastLocationDetail.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()#PastLocationForm
        
        return context

class MyFormView(FormView):
    form_class = PastLocationForm

    def form_valid(self, form): 
        print(form.cleaned_data) 
        return super().form_valid(form) 

class QueryView(FormView):
    form_class = QueryForm
    template_name = 'query_page.html'
    

    def form_valid(self, form): 
        print(form.cleaned_data) 
        return super().form_valid(form)


def profile_search(request,pk):
    items = Location.objects.filter(patient=pk)
    if request.method == 'POST':
        query_form = QueryForm(request.POST)
        if query_form.is_valid():
            model=Location
            
            #location = query_form.cleaned_data['location']
            

            period = query_form.cleaned_data['period']
            
            
            entry_list = list(Location.objects.all())
            return_dict = {}
            patient = Patient.objects.filter(pk=pk)[0]

            patient_info = str(patient).split(':')
            patient_name = patient_info[0]
            patient_confirm_date = patient_info[2]
            patient_case_number = patient_info[1]

            print(patient_info)
            print(patient_confirm_date)
            print(patient_case_number)
            patient_dict = {}
            patient_dict['patient_case_number'] = patient_case_number
            patient_dict['name'] = patient_name
            patient_dict['patient_confirm_date'] = patient_confirm_date
            

            #print(patient)
            #return_dict[-1] = 

            for location in items:

                location_str = str(location).split(' Date')[0]
            
                idx1 = str(location).find('Date From: ')
                idx2 = str(location).find(' Date To: ')
                date_from = str(location)[idx1+11:idx2]
                idx1 = str(location).find('Date To: ')
                date_to = str(location)[idx1+9:]

                date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
                date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
                
                #print(location_str)
                #print(date_from)
                #print(date_to)
                

                for i in range(len(entry_list)):
                    
                    #print(f"i is {entry_list[i].date_from}")
                    #print(f"i is {entry_list[i].date_to}")
                    #print(f"i is {entry_list[i].location_name}")
                    if location_str == entry_list[i].location_name and location.patient.idn != entry_list[i].patient.idn \
                        and not (date_from.date() > entry_list[i].date_to + datetime.timedelta(days=period) \
                        or date_to.date() < entry_list[i].date_from - datetime.timedelta(days=period)):
                        data_dict = {}
                        if date_from.date() <= entry_list[i].date_to + datetime.timedelta(days=period):

                            
                            data_dict["patient_date"] = str(date_from.date())
                            data_dict["visitor_date"] = str(entry_list[i].date_to)

                        elif date_to.date() < entry_list[i].date_from - datetime.timedelta(days=period):

                            data_dict["patient_date"] = str(date_to.date())
                            data_dict["visitor_date"] = str(entry_list[i].date_from)

                        data_dict["patient_detail"] = location.details
                        data_dict["entry_instance"] = entry_list[i]
                        print(data_dict)
                        return_dict[i] = data_dict
                        
                            


            print(return_dict)
            return render(request, 'covidapp/query_page.html',{'return_dict':return_dict, 'query_form':query_form, 'patient_dict':patient_dict})
    else:
        
        query_form = QueryForm()
    return render(request, 'covidapp/query_page.html',{'query_form':query_form})



class PatientUpdateView(UpdateView):
    form_class = PatientForm
    model = Patient

class PatientDeleteView(DeleteView):

    model = Patient
    success_url = reverse_lazy('index')

class LocationView(ListView):
    model = LocationTemplate

def location_temps(request):
    locations = LocationTemplate.objects.all()
    my_dict = {'locations':locations}
    return render(request, 'covidapp/location_list.html',context=my_dict)

class LocationDetailView(DetailView):
    model = LocationTemplate
    template_name = 'covidapp/location_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = timezone.now()
        return context

    def get_success_url(self):
        return reverse('location_detail', kwargs={'pk': self.object.pk})


class LocationUpdateView(UpdateView):
    #form_class = LocationForm
    model = LocationTemplate
    fields = ['address','district','grid_x','grid_y']
    #template_name = 'locationTemplate_update_form'

    def get_success_url(self):
        return reverse('location_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            
            for loc in Location.objects.all():
                if self.object.location_name == loc.location_name:
                    
                    setattr(loc,'address',(form.cleaned_data['address']))
                    setattr(loc,'district',(form.cleaned_data['district']))
                    setattr(loc,'grid_x',(form.cleaned_data['grid_x']))
                    setattr(loc,'grid_y',(form.cleaned_data['grid_y']))
                    
                    loc.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    


class LocationDeleteView(DeleteView):

    model = LocationTemplate
    success_url = reverse_lazy('location_list')

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        
        for loc in Location.objects.all():
            if self.object.location_name == loc.location_name:
                loc.delete()
        


        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LocationDeleteView, self).get_context_data(**kwargs)
        
        
        return context

class PLocationDetailView(DetailView):
    model = Location
    template_name = 'covidapp/plocation_detail.html'

class PLocationUpdateView(UpdateView):
    template_name = 'covidapp/plocation_update.html'
    form_class = LocationForm
    queryset = Location.objects.all()

    def get_object(self):
        id_=self.kwargs["id"]
        return get_object_or_404(Location, id=id_)

    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('plocation_detail', kwargs={'pk': self.object.pk})


    #model = Location
    #form_class = PastLocationForm
    #fields = ['date_from', 'date_to','details','category']



class PLocationDeleteView(DeleteView):
    model = Location
    #success_url = reverse('plocation_detail', kwargs={'pk': self.object.pk})

    def get_success_url(self):
        return reverse('index')
        #return reverse('plocation_detail', kwargs={'pk': self.object.pk})