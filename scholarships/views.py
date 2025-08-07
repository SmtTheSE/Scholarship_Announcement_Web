from django.views.generic import ListView, View
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from .models import ScholarshipType, Scholarship, Application
from .forms import ApplicationForm

def home(request):
    form_type = request.POST.get('form_type', '')
    login_form = AuthenticationForm()
    register_form = UserCreationForm()

    if request.method == 'POST':
        if form_type == 'login':
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                messages.success(request, f"Welcome back, {request.user.username}!")
                return redirect('scholarships:home')
            else:
                messages.error(request, "Login failed. Please check your credentials.")

        elif form_type == 'register':
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Account created successfully. You're now logged in.")
                return redirect('scholarships:home')
            else:
                messages.error(request, "Registration failed. Please correct the errors below.")

    if request.user.is_authenticated and request.user.is_staff:
        applications = Application.objects.filter(status='submitted').select_related('user', 'scholarship').order_by('-created_at')
        return render(request, 'scholarships/admin_dashboard.html', {
            'applications': applications
        })

    rejection_notice = None
    if request.user.is_authenticated:
        rejected_app = Application.objects.filter(user=request.user, status='rejected').order_by('-updated_at').first()
        if rejected_app:
            rejection_notice = rejected_app.rejection_reason

    return render(request, 'home.html', {
        'login_form': login_form,
        'register_form': register_form,
        'rejection_notice': rejection_notice,
    })


@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('scholarships:home')


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


class ScholarshipDetailView(View):
    def get(self, request, pk):
        scholarship = get_object_or_404(Scholarship, pk=pk)
        application = None
        form = None

        if request.user.is_authenticated:
            application = Application.objects.filter(scholarship=scholarship, user=request.user).first()

        if application and application.status == 'rejected':
            return render(request, 'scholarships/detail.html', {
                'scholarship': scholarship,
                'application': application,
                'application_form': None,
                'rejection_reason': application.rejection_reason,
            })

        if request.user.is_authenticated:
            form = ApplicationForm(instance=application)

        return render(request, 'scholarships/detail.html', {
            'scholarship': scholarship,
            'application_form': form,
            'application': application,
        })

    def post(self, request, pk):
        scholarship = get_object_or_404(Scholarship, pk=pk)
        application = Application.objects.filter(scholarship=scholarship, user=request.user).first()

        if application and application.status == 'rejected':
            messages.error(request, "You cannot edit a rejected application.")
            return redirect('scholarships:detail', pk=pk)

        form = ApplicationForm(request.POST, request.FILES, instance=application)

        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.scholarship = scholarship

            action = request.POST.get("action")
            if action == "submit":
                app.status = "submitted"
            else:
                app.status = "draft"

            app.save()
            messages.success(request, "Application saved successfully.")
            return redirect('scholarships:detail', pk=pk)
        else:
            messages.error(request, "There was an error with your application.")

        return render(request, 'scholarships/detail.html', {
            'scholarship': scholarship,
            'application_form': form,
            'application': application,
        })


@login_required
@require_POST
def bookmark_scholarship(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    scholarship.bookmarked_by.add(request.user)
    return redirect('scholarships:detail', pk=pk)


@login_required
def my_bookmarks(request):
    bookmarks = request.user.bookmarks.all()
    return render(request, 'bookmarks.html', {'bookmarks': bookmarks})


@csrf_protect
@require_POST
@login_required
def review_application(request, app_id):
    if not request.user.is_staff:
        return redirect('scholarships:home')

    application = get_object_or_404(Application, id=app_id, status='submitted')
    decision = request.POST.get('decision')
    reason = request.POST.get('reason')

    if decision == 'accept':
        application.status = 'accepted'
        application.rejection_reason = ''
        messages.success(request, f"Application from {application.user.username} has been accepted.")
    elif decision == 'reject':
        application.status = 'rejected'
        application.rejection_reason = reason or 'No reason provided.'
        messages.warning(request, f"Application from {application.user.username} has been rejected.")

    application.save()
    return redirect('scholarships:home')