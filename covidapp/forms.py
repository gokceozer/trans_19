from django import forms
from django.forms import modelformset_factory
from covidapp.models import Patient, Location, LocationTemplate
from trans19 import settings
from crispy_forms.helper import FormHelper

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    date_of_confirm = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Patient
        fields = '__all__'
        labels = {
        "idn": "Identity Document Number"
        }

class LocationForm(forms.ModelForm):
    
    class Meta:
        model = LocationTemplate
        #exclude = ('patient',)
        fields=['location_name', 'address','district', 'grid_x','grid_y']

class PastLocationForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=LocationTemplate.objects.all().order_by('location_name'))
    class Meta:
        model = Location
        #exclude = ('patient',)
        exclude=['location_name', 'address','district', 'grid_x','grid_y', 'patient']



class QueryForm(forms.Form):
    period = forms.IntegerField()
    location = forms.ModelChoiceField(queryset=LocationTemplate.objects.all().order_by('location_name'))
    #location = forms.CharField(max_length=100, required = False)
    