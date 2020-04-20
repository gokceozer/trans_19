from django.shortcuts import render
from covidapp.forms import PatientForm, LocationFormSet, QueryForm
from covidapp.models import Patient, Location
from django.views.generic import DetailView, ListView, FormView
from . import forms
from django.http import HttpResponseRedirect
import datetime

# Create your views here.
def index(request):
    patient_dict = Patient.objects.order_by('case_number')
    my_dict = {'patients':patient_dict}
    return render(request, 'covidapp/index.html',context=my_dict)


def patient_new(request):
    patientForm = PatientForm()
    formset = LocationFormSet()
    if request.method == "POST":
        patientForm = PatientForm(request.POST)
        formset = LocationFormSet(request.POST) 
        if patientForm.is_valid() and formset.is_valid():
            patient = patientForm.save(commit=True)
            for form in formset:
                location = form.save(commit=False)
                location.patient = patient
                location.save()
            return index(request)
        else:
            print('ERROR FORM INVALID')

    return render(request, 'covidapp/patient_new.html',{'patientForm':patientForm, 'formset':formset})

class PatientDetailView(DetailView):
    model=Patient


def profile_search(request):
    if request.method == 'POST': 
        query_form = QueryForm(request.POST)
        if query_form.is_valid():
            model=Location
            #print(query_form.cleaned_data['period'])

            entry_list = list(Location.objects.all())
            return_dict = {}
            counter = 0
            #print(len(entry_list))
            for i in range(len(entry_list)):
                #print(f"i is {i}")
                
                no_result = True
                for j in range(i, len(entry_list)):
                    '''print(type(entry_list[j].date_to))
                    print(entry_list[i].date_to)
                    print(entry_list[i].patient.name)'''
                    if not (entry_list[i].date_from > entry_list[j].date_to + datetime.timedelta(days=2) or entry_list[i].date_to < entry_list[j].date_from - datetime.timedelta(days=2)) and entry_list[i].patient.idn != entry_list[j].patient.idn and entry_list[i].location_name == entry_list[j].location_name:
                        
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
                
                
                

            #print(return_dict)
            return render(request, 'covidapp/query_page.html',{'return_dict':return_dict, 'query_form':query_form})
                
            #return HttpResponseRedirect('/thanks/') 
    else:
        query_form = QueryForm()

    return render(request, 'covidapp/query_page.html',{'query_form':query_form})

