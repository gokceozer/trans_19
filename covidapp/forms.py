from django import forms
from django.forms import modelformset_factory
from covidapp.models import Patient, Location
from trans19 import settings

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    date_of_confirm = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Patient
        fields = '__all__'

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
        exclude = ('patient',)

LocationFormSet = modelformset_factory(
    Location,
    form=LocationForm,
    extra=1,
    exclude = ('patient',),
    #fields=('location_name','address','grid_x','grid_y','date_from','date_to','details','category'),
    widgets = {
    'date_from': forms.DateInput(format='%d-%m-%Y'),
    'date_to': forms.DateInput(format='%d-%m-%Y'),
    },
)


class QueryForm(forms.Form):
    period = forms.IntegerField()
    location = forms.CharField(max_length=100, required = False)
    date_from = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required = False)
    date_to = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required = False)
    