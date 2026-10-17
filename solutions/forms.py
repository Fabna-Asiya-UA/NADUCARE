from django import forms
from .models import Solution


class SolutionForm(forms.ModelForm):

    class Meta:
        model = Solution
        fields = ['description']

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Suggest a practical solution...',
            }),
        }

    def clean_description(self):
        description = self.cleaned_data['description'].strip()

        if len(description) < 10:
            raise forms.ValidationError(
                'Please provide at least 10 characters.'
            )

        return description