from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import ScholarshipType, Scholarship
from django.contrib import messages



def home(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                messages.success(request, f"Welcome back, {request.user.username}!")
                return redirect('scholarships:home')

        elif form_type == 'register':
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('scholarships:home')  # ✅ Redirect to homepage after register

    return render(request, 'home.html', {
        'login_form': login_form,
        'register_form': register_form,
    })


@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('scholarships:home')  # ✅ Always redirect to clean homepage


class TypeListView(ListView):
    model = ScholarshipType
    template_name = 'scholarships/type_list.html'
    context_object_name = 'types'

    def get_queryset(self):
        return ScholarshipType.objects.all()


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


@login_required
def bookmark_scholarship(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    scholarship.bookmarked_by.add(request.user)
    return redirect('scholarships:detail', pk=pk)


@login_required
def my_bookmarks(request):
    bookmarks = request.user.bookmarks.all()
    return render(request, 'bookmarks.html', {'bookmarks': bookmarks})
