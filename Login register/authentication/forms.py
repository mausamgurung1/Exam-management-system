from django import forms
from .models import StudentMark

class StudentMarkForm(forms.ModelForm):
    class Meta:
        model = StudentMark
        fields = ['subject', 'full_marks', 'obtained_marks']

from django import forms
from .models import StudentMark

class StudentMarkForm(forms.ModelForm):
    class Meta:
        model = StudentMark
        fields = ['obtained_marks']
        widgets = {
            'obtained_marks': forms.NumberInput(attrs={'min': 0, 'max': 100, 'style': 'width: 80px;'}),
        }
