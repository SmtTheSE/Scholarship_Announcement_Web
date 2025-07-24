# scholarships/admin.py

from django.contrib import admin
from .models import ScholarshipType, Scholarship

@admin.register(ScholarshipType)
class ScholarshipTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'type', 'deadline')
    list_filter = ('type', 'deadline')
    search_fields = ('title', 'provider')

