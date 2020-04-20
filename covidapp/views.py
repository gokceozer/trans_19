from django.shortcuts import render
from covidapp.forms import PatientForm, LocationFormSet
from covidapp.models import Patient, Location
from django.views.generic import DetailView
from . import forms

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
