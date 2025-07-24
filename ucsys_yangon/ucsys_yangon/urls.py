from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('scholarships/', include('scholarships.urls', namespace='scholarships')),
    path('admin/', admin.site.urls),
]