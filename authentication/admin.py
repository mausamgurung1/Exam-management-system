from django.contrib import admin
from .models import Profile, Attendance, InternalMark, SEMESTER_SUBJECT_MAP
from django import forms

class InternalMarkForm(forms.ModelForm):
    class Meta:
        model = InternalMark
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        semester = None

        # Try to get the semester from the instance (editing existing) or from form data (adding new)
        if self.instance and self.instance.pk:
            semester = self.instance.semester
        elif 'semester' in self.data:
            try:
                semester = int(self.data.get('semester'))
            except (ValueError, TypeError):
                pass

        if semester:
            subjects = SEMESTER_SUBJECT_MAP.get(semester, [])
            self.fields['subject'].widget = forms.Select(choices=[(s, s) for s in subjects])
        else:
            self.fields['subject'].widget = forms.Select(choices=[])  # empty if semester not chosen yet

class InternalMarkAdmin(admin.ModelAdmin):
    form = InternalMarkForm
    list_display = ('profile', 'semester', 'subject', 'theory_obtained_marks', 'practical_obtained_marks')

admin.site.register(InternalMark, InternalMarkAdmin)  # ✅ Keep this one

admin.site.register(Profile)
admin.site.register(Attendance)
# admin.site.register(InternalMark)  # ❌ Remove or comment out this line

