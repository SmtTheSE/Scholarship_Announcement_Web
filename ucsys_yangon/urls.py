from django.contrib import admin
from django.template.backends import django
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language



urlpatterns = [
    path('', include(('scholarships.urls', 'scholarships'), namespace='scholarships')),  # 👈 homepage and app
    path('admin/', admin.site.urls),
    path('set_language/', set_language, name='set_language'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
