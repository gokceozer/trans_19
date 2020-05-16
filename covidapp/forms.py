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

DISTRICT_CHOICES= [
    ('orange', 'Central and Western'),
    ('cantaloupe', 'Eastern'),
    ('mango', 'Southern'),
    ('honeydew', 'Wan Chai'),
    ('honeydew', 'Kowloon City'),
    ('honeydew', 'Kwun Tong'),
    ('honeydew', 'Sham Shui Po'),
    ('honeydew', 'Wong Tai Sin'),
    ('honeydew', 'Yau Tsim Mong'),
    ('honeydew', 'Islands'),
    ('honeydew', 'Kwai Tsing'),
    ('honeydew', 'North'),
    ('honeydew', 'Sai Kung'),
    ('honeydew', 'Sha Tin'),
    ('honeydew', 'Tai Po'),
    ('honeydew', 'Tsuen Wan'),
    ('honeydew', 'Tuen Mun'),
    ('honeydew', 'Yuen Long'),
    ]


class LocationForm(forms.ModelForm):
    district= forms.CharField(label='District', widget=forms.Select(choices=DISTRICT_CHOICES))

    
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
    period = forms.IntegerField(initial=0)
    #location = forms.ModelChoiceField(queryset=Location.objects.all().order_by('location_name'))
    #location = forms.CharField(max_length=100, required = False) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['location'].queryset = items.order_by('location_name')


class LocationForm(forms.ModelForm):
    date_from = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            attrs={'class': 'date'},
            format='%d-%m-%Y'
        )
    )

    date_to = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            attrs={'class': 'date'},
            format='%d-%m-%Y'
        )
    )

    class Meta:
        model = Location
        fields = '__all__'
        #exclude = ('patient',)