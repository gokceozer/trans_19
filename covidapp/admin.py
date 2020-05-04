from django.contrib import admin
from covidapp.models import Patient,Location, LocationTemplate
# Register your models here.

admin.site.register(Patient)
admin.site.register(Location)
admin.site.register(LocationTemplate)