from django.shortcuts import render
from covidapp.forms import PatientForm, QueryForm, LocationForm #LocationFormSet
from covidapp.models import Patient, Location
from django.views.generic import DetailView, ListView, FormView, UpdateView, DeleteView
from . import forms
from django.http import HttpResponseRedirect
import datetime
from collections import OrderedDict
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    patient_dict = Patient.objects.order_by('case_number')
    my_dict = {'patients':patient_dict}
    return render(request, 'covidapp/index.html',context=my_dict)


def patient_new(request):
    patientForm = PatientForm()
    #formset = LocationFormSet()
    if request.method == "POST":
        patientForm = PatientForm(request.POST)
        #formset = LocationFormSet(request.POST) 
        if patientForm.is_valid(): #and formset.is_valid():
            patientForm.save(commit=True)
            '''patient = patientForm.save(commit=True)
            for form in formset:
                location = form.save(commit=False)
                location.patient = patient
                location.save()'''
            return index(request)
        else:
            print('ERROR FORM INVALID')
#, 'formset':formset
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



class PatientDetailView(DetailView):
    model=Patient


def profile_search(request):
    if request.method == 'POST': 
        query_form = QueryForm(request.POST)
        if query_form.is_valid():
            model=Location
            period = query_form.cleaned_data['period']
            loc_name = query_form.cleaned_data['location']
            date_f = query_form.cleaned_data['date_from']
            date_t = query_form.cleaned_data['date_to']

            entry_list = list(Location.objects.all())
            #return_dict = {}
            return_dict = OrderedDict()

            counter = 1
            #print(len(entry_list))
            for i in range(len(entry_list)):
                #print(f"i is {i}")
                
                no_result = True
                for j in range(i, len(entry_list)):
                    '''print(type(entry_list[j].date_to))
                    print(entry_list[i].date_to)
                    print(entry_list[i].patient.name)'''
                    if not (entry_list[i].date_from > entry_list[j].date_to + datetime.timedelta(days=period) \
                            or entry_list[i].date_to < entry_list[j].date_from - datetime.timedelta(days=period)) \
                            and entry_list[i].patient.idn != entry_list[j].patient.idn \
                            and entry_list[i].location_name == entry_list[j].location_name:
                        
                        if no_result:
                            return_dict[counter] = entry_list[i]
                            counter+=1
                            return_dict[counter] = entry_list[j]
                            counter+=1
                        else:
                            return_dict[counter] = entry_list[j]
                            counter+=1

                        no_result = False

                if no_result:
                    continue

                return_dict[counter] = "done"
                counter+=1
            

            '''my_list = []
            if loc_name != "":
                #print(loc_name)
                my_list = list(return_dict.items())
                print(my_list)       
                for i in my_list:
                    #print(i)
                    if i[1] != loc_name:
                        
                        my_list.remove(i)
            else:
                print('No location indicated')'''

            #print(my_list)

                
                
            if return_dict[next(reversed(return_dict))] == 'done':
                return_dict.popitem()

            #print(return_dict)
            return render(request, 'covidapp/query_page.html',{'return_dict':return_dict, 'query_form':query_form})
                
    else:
        query_form = QueryForm()

    return render(request, 'covidapp/query_page.html',{'query_form':query_form})

class PatientUpdateView(UpdateView):
    #redirect_field_name = 'trans_19/patient_detail.html'
    print("YOOO")
    #fields = ('name',)
    form_class = PatientForm

    model = Patient



class PatientDeleteView(DeleteView):
    print("HELLO")
    model = Patient
    success_url = reverse_lazy('index')