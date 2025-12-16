from django import forms
from .models import Student, Teacher, Class, Subject, Fees, Salary, StudentAttendance, TeacherAttendance, Admin


class LoginForm(forms.Form):
    """Login form for all user types"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'id': 'role'
    }))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username',
        'id': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
        'id': 'password'
    }))


class StudentForm(forms.ModelForm):
    """Form for adding/editing students"""
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password (leave blank to keep current)'
    }))
    
    class Meta:
        model = Student
        exclude = ['created_at', 'updated_at']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Roll Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'student_class': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Section'}),
            'admission_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admission Number'}),
            'admission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Name'}),
            'parent_mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Mobile'}),
            'parent_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Parent Email'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            instance.set_password(password)
        if commit:
            instance.save()
        return instance


class TeacherForm(forms.ModelForm):
    """Form for adding/editing teachers"""
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password (leave blank to keep current)'
    }))
    
    class Meta:
        model = Teacher
        exclude = ['created_at', 'updated_at', 'subjects']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qualification'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'}),
        }

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        qs = Teacher.objects.filter(employee_id=employee_id)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "This Employee ID already exists. Please use a unique Employee ID."
            )

        return employee_id

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            instance.set_password(password)
        if commit:
            instance.save()
        return instance


class ClassForm(forms.ModelForm):
    """Form for adding/editing classes"""
    class Meta:
        model = Class
        fields = ['name', 'section']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class Name (e.g., Class 1)'}),
            'section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Section (e.g., A, B)'}),
        }


class SubjectForm(forms.ModelForm):
    """Form for adding/editing subjects"""
    class Meta:
        model = Subject
        fields = ['name', 'code', 'class_assigned']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Code'}),
            'class_assigned': forms.Select(attrs={'class': 'form-control'}),
        }


class FeesForm(forms.ModelForm):
    """Form for adding/editing fees"""
    class Meta:
        model = Fees
        fields = ['student', 'fee_type', 'amount', 'due_date', 'paid_date', 'paid_amount', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'fee_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fee Type'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Paid Amount'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Remarks'}),
        }


class SalaryForm(forms.ModelForm):
    """Form for adding/editing salary"""
    class Meta:
        model = Salary
        fields = ['teacher', 'month', 'amount', 'paid_date', 'status', 'remarks']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Month (e.g., January 2024)'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'paid_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Remarks'}),
        }


class StudentAttendanceForm(forms.ModelForm):
    """Form for student attendance"""
    class Meta:
        model = StudentAttendance
        fields = ['student', 'date', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Remarks'}),
        }


class TeacherAttendanceForm(forms.ModelForm):
    """Form for teacher attendance"""
    class Meta:
        model = TeacherAttendance
        fields = ['teacher', 'date', 'status', 'remarks']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Remarks'}),
        }
