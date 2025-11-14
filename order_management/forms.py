from django import forms
from .models import OrderManagement

class OrderManagementAdminForm(forms.ModelForm):
    class Meta:
        model = OrderManagement
        fields = '__all__'
        widgets = {
            'project_case_title': forms.TextInput(attrs={
                'style': 'width: 100%; min-width: 600px; padding: 8px; font-size: 14px;',
                'class': 'vTextField',
            }),
            'payment_information': forms.Textarea(attrs={
                'rows': 4,
                'cols': 80,
                'style': 'width: 100%; min-width: 600px; padding: 8px; font-size: 14px;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make currency field read-only since it's always SAR
        self.fields['currency'].widget.attrs['readonly'] = True