# scholarships/urls.py

from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'scholarships'

urlpatterns = [
    path('', views.TypeListView.as_view(), name='type_list'),
    path('type/<int:pk>/', views.ScholarshipListView.as_view(), name='list_by_type'),
    path('program/<int:pk>/', views.ScholarshipDetailView.as_view(), name='detail'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

]


