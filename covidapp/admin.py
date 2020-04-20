from django.contrib import admin
from covidapp.models import Patient,Location
# Register your models here.

admin.site.register(Patient)
admin.site.register(Location)