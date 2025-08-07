from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

class ScholarshipType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Scholarship(models.Model):
    type = models.ForeignKey(ScholarshipType, on_delete=models.CASCADE, related_name='programs')
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=150)
    description = models.TextField()
    opportunities = models.TextField(help_text="List opportunities separated by line breaks")
    deadline = models.DateField()
    attachment = models.FileField(upload_to='scholarship_pdfs/', blank=True, null=True)

    def get_opportunities_list(self):
        return [o.strip() for o in self.opportunities.splitlines() if o.strip()]

    def __str__(self):
        return f"{self.title} ({self.provider})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    statement = RichTextField()
    cv = models.FileField(upload_to='applications/cv/', blank=True, null=True)
    certificate = models.FileField(upload_to='applications/certificates/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'scholarship')

    def __str__(self):
        return f"{self.user.username} - {self.scholarship.title} ({self.status})"
