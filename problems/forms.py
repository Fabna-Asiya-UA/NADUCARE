
from django import forms
from .models import Problem


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'title',
            'description',
            'district',
            'category',
            'location',
            'photo',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter problem title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain the problem clearly',
            }),
            'district': forms.Select(attrs={
                'class': 'form-select',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter area or landmark',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
