from django.urls import path
from . import views

app_name = 'scholarships'

urlpatterns = [
    path('', views.home, name='home'),  # 👈 homepage view
    path('logout/', views.logout_view, name='logout'),
    path('types/', views.TypeListView.as_view(), name='type_list'),
    path('type/<int:pk>/', views.ScholarshipListView.as_view(), name='list_by_type'),
    path('program/<int:pk>/', views.ScholarshipDetailView.as_view(), name='detail'),
    path('review/<int:app_id>/', views.review_application, name='review_application')
]
