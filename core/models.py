from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Class(models.Model):
    """Class/Grade model"""
    name = models.CharField(max_length=50)  # e.g., "Class 1", "Class 10"
    section = models.CharField(max_length=10, blank=True)  # e.g., "A", "B"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['name', 'section']

    def __str__(self):
        if self.section:
            return f"{self.name} - {self.section}"
        return self.name


class Subject(models.Model):
    """Subject model"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Teacher(models.Model):
    """Teacher model"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    employee_id = models.CharField(max_length=50, unique=True)
    qualification = models.CharField(max_length=200, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    experience = models.CharField(max_length=50, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subjects = models.ManyToManyField(Subject, blank=True, related_name='teachers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.employee_id})"

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"


class Student(models.Model):
    """Student model"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    roll_no = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')
    section = models.CharField(max_length=10, blank=True)
    admission_no = models.CharField(max_length=50, unique=True)
    admission_date = models.DateField(null=True, blank=True)
    parent_name = models.CharField(max_length=100, blank=True)
    parent_mobile = models.CharField(max_length=15, blank=True)
    parent_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.admission_no})"

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"


class Admin(models.Model):
    """Admin model"""
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} {self.surname}"

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"


class StudentAttendance(models.Model):
    """Student attendance model"""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class TeacherAttendance(models.Model):
    """Teacher attendance model"""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['teacher', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.teacher} - {self.date} - {self.status}"


class Fees(models.Model):
    """Student fees model"""
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=50)  # e.g., "Tuition", "Exam", "Library"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Fees"

    def __str__(self):
        return f"{self.student} - {self.fee_type} - {self.status}"


class Salary(models.Model):
    """Teacher salary model"""
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='salaries')
    month = models.CharField(max_length=20)  # e.g., "January 2024"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Salaries"
        unique_together = ['teacher', 'month']

    def __str__(self):
        return f"{self.teacher} - {self.month} - {self.status}"
