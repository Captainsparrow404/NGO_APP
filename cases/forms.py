from django import forms
from .models import Case

class CaseAdminForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['case_name', 'featured_image', 'description', 'status']  # Explicitly exclude modified_date
        widgets = {
            'case_name': forms.Textarea(attrs={
                'rows': 3,
                'cols': 80,
                'style': 'width: 100%; min-width: 800px; height: 30px; padding: 12px; font-size: 14px; resize: horizontal; border: 2px solid #ddd; border-radius: 6px;',
                'class': 'vLargeTextField bilingual-field',
                'dir': 'auto',
                'placeholder': 'Enter case name...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Additional customization for case_name field
        self.fields['case_name'].widget.attrs.update({
            'style': 'width: 100%; min-width: 800px; height: 30px; padding: 12px; font-size: 14px; resize: horizontal; border: 2px solid #ddd; border-radius: 6px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
            'onfocus': 'this.style.borderColor="#417690"; this.style.boxShadow="0 0 0 3px rgba(65, 118, 144, 0.1)";',
            'onblur': 'this.style.borderColor="#ddd"; this.style.boxShadow="none";'
        })