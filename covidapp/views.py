from django.shortcuts import render
from covidapp.forms import PatientForm, QueryForm, LocationForm, PastLocationForm #LocationFormSet
from covidapp.models import Patient, Location
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

def profile_search(request,pk):
    if request.method == 'POST': 
        query_form = QueryForm(request.POST)
        if query_form.is_valid():
            model=Location
            location = query_form.cleaned_data['location']
            period = query_form.cleaned_data['period']
            
            
            entry_list = list(Location.objects.all())
            return_dict = {}


            #print(len(entry_list))
            for i in range(len(entry_list)):
                print(f"i is {entry_list[i].date_from}")
                print(f"i is {entry_list[i].date_to}")
                print(f"i is {entry_list[i].location_name}")
                '''for j in range(i, len(entry_list)):
                    print(type(entry_list[j].date_to))
                    print(entry_list[i].date_to)
                    print(entry_list[i].patient.name)
                    if not (entry_list[i].date_from > entry_list[j].date_to + datetime.timedelta(days=period) \
                            or entry_list[i].date_to < entry_list[j].date_from - datetime.timedelta(days=period)) \
                            and entry_list[i].patient.idn != entry_list[j].patient.idn \
                            and entry_list[i].location_name == entry_list[j].location_name:
                        
                        if no_result:
                            return_dict[counter] = entry_list[i]
                            
                            return_dict[counter] = entry_list[j]
                            
                        else:
                            return_dict[counter] = entry_list[j]'''
                            
        
            '''if return_dict[next(reversed(return_dict))] == 'done':
                return_dict.popitem()'''

            #print(return_dict)
            return render(request, 'covidapp/query_page.html',{'return_dict':return_dict, 'query_form':query_form})
                
    else:
        query_form = QueryForm()

    return render(request, 'covidapp/query_page.html',{'query_form':query_form})

class PatientUpdateView(UpdateView):
    form_class = PatientForm
    model = Patient

class PatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy('index')