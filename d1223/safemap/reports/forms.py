from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    happened_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type':'datetime-local'}),
        label='발생 시간'
    )
    class Meta:
        model = Report
        fields = ('title','content','lat','lng','happened_at', 'address_text', 'sido', 'sigungu', 'dong')
        widgets = {
            'content': forms.Textarea(attrs={'rows':5}),
        }
