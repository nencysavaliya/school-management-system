from django.contrib import admin
from .models import Class, Subject, Teacher, Student, Admin, StudentAttendance, TeacherAttendance, Fees, Salary


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'created_at']
    search_fields = ['name', 'section']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'class_assigned', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['class_assigned']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'surname', 'email', 'mobile', 'joining_date']
    search_fields = ['name', 'surname', 'employee_id', 'email']
    list_filter = ['gender', 'joining_date']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_no', 'name', 'surname', 'roll_no', 'student_class', 'section']
    search_fields = ['name', 'surname', 'admission_no', 'roll_no']
    list_filter = ['student_class', 'section', 'gender']


@admin.register(Admin)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'surname', 'email', 'created_at']
    search_fields = ['username', 'name', 'surname', 'email']


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'marked_by']
    search_fields = ['student__name', 'student__surname']
    list_filter = ['status', 'date']


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'date', 'status']
    search_fields = ['teacher__name', 'teacher__surname']
    list_filter = ['status', 'date']


@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_type', 'amount', 'due_date', 'status']
    search_fields = ['student__name', 'student__surname', 'fee_type']
    list_filter = ['status', 'fee_type']


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'month', 'amount', 'status', 'paid_date']
    search_fields = ['teacher__name', 'teacher__surname']
    list_filter = ['status', 'month']
