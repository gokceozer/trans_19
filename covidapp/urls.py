from django.contrib import admin
from django.urls import path, re_path
from covidapp import views
from django.conf.urls import url
from django.views.decorators.http import require_POST

urlpatterns = [
    path('index/', views.index, name='index'),
    path('patient_new/', views.patient_new, name='patient_new'),
    path('location_new/', views.location_new, name='location_new'),
    path('location_list/', views.location_temps, name='location_list'),
    re_path('patient/(?P<pk>\d+)$', views.PatientDetailView.as_view(), name='patient_detail'),
    re_path('location/(?P<pk>\d+)$', views.LocationDetailView.as_view(), name='location_detail'),
    re_path('patient/(?P<pk>\d+)/edit/$', views.PatientUpdateView.as_view(), name='patient_edit'),
    re_path('my_form/$', require_POST(views.MyFormView.as_view()), name='my_form_view_url'),
    re_path('patient/(?P<pk>\d+)/remove/$', views.PatientDeleteView.as_view(), name='patient_remove'),
    re_path('patient/(?P<pk>\d+)/query/$', views.profile_search, name='query'),
    #re_path('patient/(?P<pk>\d+)/query/$', views.QueryView.as_view(), name='query'),
    re_path('location/(?P<pk>\d+)/edit/$', views.LocationUpdateView.as_view(), name='location_edit'),
    re_path('location/(?P<pk>\d+)/remove/$', views.LocationDeleteView.as_view(), name='location_remove'),
    re_path('location/(?P<pk>\d+)/plocation/$', views.PLocationDetailView.as_view(), name='plocation_detail'),
    #re_path('location/(?P<pk>\d+)/editPL/$', views.PLocationUpdateView.as_view(), name='plocation_edit'),
    path('location/<int:id>/editPL/',views.PLocationUpdateView.as_view(), name='plocation_edit'),
    re_path('location/(?P<pk>\d+)/removePL/$', views.PLocationDeleteView.as_view(), name='plocation_remove'),
]
