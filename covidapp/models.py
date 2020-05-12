from django.db import models
from django.urls import reverse
# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=200)
    idn = models.CharField(max_length=200, unique=True)
    date_of_birth = models.DateField()
    date_of_confirm = models.DateField()
    case_number = models.IntegerField()

    def get_absolute_url(self):
        return reverse("patient_detail", kwargs={'pk':self.pk})

    

    def __str__(self):
        return self.name + ":" + str(self.case_number) + ":" + str(self.date_of_confirm)

class Location(models.Model):
    patient = models.ForeignKey(Patient, related_name='locations', on_delete=models.CASCADE, null=True, blank=True)
    location_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    district = models.CharField(max_length=300, null=True, blank=True)
    grid_x = models.IntegerField(null=True, blank=True)
    grid_y = models.IntegerField(null=True, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    details = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.location_name) + ' Date From: ' + str(self.date_from) + ' Date To: ' + str(self.date_to) 


class LocationTemplate(models.Model):
    location_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    district = models.CharField(max_length=300, null=True, blank=True)
    grid_x = models.IntegerField(null=True, blank=True)
    grid_y = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return self.location_name + ", Address: " + self.address + ", District: " + self.district + ", Coordinates: (" + str(self.grid_x) + ", " + str(self.grid_y) + ")"