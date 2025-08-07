from django.contrib import admin
from .models import ScholarshipType, Scholarship, Application

@admin.register(ScholarshipType)
class ScholarshipTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'provider', 'deadline')
    list_filter = ('type', 'deadline')
    search_fields = ('title', 'provider')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'scholarship', 'status',
        'created_at', 'updated_at', 'rejection_reason'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'scholarship__title')
    readonly_fields = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'submitted':
            return self.readonly_fields + (
                'user', 'scholarship', 'status',
                'statement', 'cv', 'certificate', 'rejection_reason'
            )
        return self.readonly_fields

    fieldsets = (
        (None, {
            'fields': ('user', 'scholarship', 'status')
        }),
        ('Application Content', {
            'fields': ('statement', 'cv', 'certificate')
        }),
        ('Review Notes', {
            'fields': ('rejection_reason',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
