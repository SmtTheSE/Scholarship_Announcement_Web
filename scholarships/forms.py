from django import forms
from .models import Application
from ckeditor.widgets import CKEditorWidget

class ApplicationForm(forms.ModelForm):
    statement = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Application
        fields = ['statement', 'cv', 'certificate']
        widgets = {
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }