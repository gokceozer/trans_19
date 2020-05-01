from django.contrib import admin
from django.urls import path, re_path
from covidapp import views
from django.conf.urls import url
from django.views.decorators.http import require_POST

urlpatterns = [
    path('', views.index, name='index'),
    path('patient_new/', views.patient_new, name='patient_new'),
    path('location_new/', views.location_new, name='location_new'),
    re_path('patient/(?P<pk>\d+)$', views.PatientDetailView.as_view(), name='patient_detail'),
    path('query/', views.profile_search, name='query'),
    #url(r'^patient/(?P<pk>\d+)/remove/$', views.PatientDeleteView.as_view(), name='patient_remove'),
    re_path('patient/(?P<pk>\d+)/edit/$', views.PatientUpdateView.as_view(), name='patient_edit'),
    re_path('my_form/$', require_POST(views.MyFormView.as_view()), name='my_form_view_url'),
    re_path('patient/(?P<pk>\d+)/remove/$', views.PatientDeleteView.as_view(), name='patient_remove'),
    
]
