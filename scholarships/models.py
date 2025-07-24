# scholarships/models.py

from django.db import models

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
    opportunities = models.TextField(
        help_text="List opportunities separated by line breaks"
    )
    deadline = models.DateField()
    attachment = models.FileField(upload_to='scholarship_pdfs/', blank=True, null=True)

    def get_opportunities_list(self):
        return [o.strip() for o in self.opportunities.splitlines() if o.strip()]

    def __str__(self):
        return f"{self.title} ({self.provider})"

