# scholarships/views.py

from django.views.generic import ListView, DetailView
from .models import ScholarshipType, Scholarship

class TypeListView(ListView):
    model = ScholarshipType
    template_name = 'scholarships/type_list.html'
    context_object_name = 'types'

    def get_queryset(self):
        qs = ScholarshipType.objects.all()
        print("Loaded categories:", qs)
        return qs  # ← updated

class ScholarshipListView(ListView):
    model = Scholarship
    template_name = 'scholarships/program_list.html'
    context_object_name = 'scholarships'

    def get_queryset(self):
        qs = Scholarship.objects.filter(type_id=self.kwargs['pk'])
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(title__icontains=query) | qs.filter(provider__icontains=query)
        return qs

class ScholarshipDetailView(DetailView):
    model = Scholarship
    template_name = 'scholarships/detail.html'

