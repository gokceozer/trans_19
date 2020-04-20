from django.contrib import admin
from django.urls import path, re_path
from covidapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('patient_new/', views.patient_new, name='patient_new'),
    re_path('patient/(?P<pk>\d+)', views.PatientDetailView.as_view(), name='patient_detail'),
]
