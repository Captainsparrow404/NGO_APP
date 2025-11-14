from django import forms
from .models import ProjectManagement

class ProjectManagementAdminForm(forms.ModelForm):
    class Meta:
        model = ProjectManagement
        fields = ['project_name', 'featured_image', 'description', 'end_date', 'goal_amount', 'status']
        widgets = {
            'project_name': forms.Textarea(attrs={
                'rows': 3,
                'cols': 80,
                'style': 'width: 100%; min-width: 800px; height: 30px; padding: 12px; font-size: 14px; resize: horizontal; border: 2px solid #ddd; border-radius: 6px;',
                'class': 'vLargeTextField bilingual-field',
                'dir': 'auto',
                'placeholder': 'Enter project name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bilingual-field',
                'dir': 'auto',
                'required': False  # Make description not required in the form
            }),
            'end_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'style': 'width: 200px; padding: 5px;'
                }
            ),
            'goal_amount': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'style': 'width: 200px;'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Additional customization for project_name field
        self.fields['project_name'].widget.attrs.update({
            'style': 'width: 100%; min-width: 800px; height: 30px; padding: 12px; font-size: 14px; resize: horizontal; border: 2px solid #ddd; border-radius: 6px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
            'onfocus': 'this.style.borderColor="#417690"; this.style.boxShadow="0 0 0 3px rgba(65, 118, 144, 0.1)";',
            'onblur': 'this.style.borderColor="#ddd"; this.style.boxShadow="none";'
        })
        self.fields['description'].required = False