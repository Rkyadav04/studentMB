from django import forms
from .models import Student
from django.core.exceptions import ValidationError
    
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Student
        fields =  ['student_id', 'name', 'course', 'contact', 'email', 'last_result', 'status','is_deleted',]
