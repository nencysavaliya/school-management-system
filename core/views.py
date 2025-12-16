from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from .models import (
    Student, Teacher, Class, Subject, Admin,
    StudentAttendance, TeacherAttendance, Fees, Salary
)
from .forms import (
    LoginForm, StudentForm, TeacherForm, ClassForm, SubjectForm,
    FeesForm, SalaryForm, StudentAttendanceForm, TeacherAttendanceForm
)


# ==================== HOME & AUTH ====================

def home(request):
    """Home page view"""
    return render(request, 'home.html')


def login_view(request):
    """Unified login view for Admin, Teacher, and Student"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if role == 'admin':
                try:
                    admin = Admin.objects.get(username=username)
                    if admin.check_password(password):
                        request.session['user_id'] = admin.id
                        request.session['user_role'] = 'admin'
                        request.session['user_name'] = admin.full_name
                        messages.success(request, f'Welcome, {admin.full_name}!')
                        return redirect('admin_dashboard')
                    else:
                        messages.error(request, 'Invalid password!')
                except Admin.DoesNotExist:
                    messages.error(request, 'Admin not found!')
                    
            elif role == 'teacher':
                try:
                    teacher = Teacher.objects.get(username=username)
                    if teacher.check_password(password):
                        request.session['user_id'] = teacher.id
                        request.session['user_role'] = 'teacher'
                        request.session['user_name'] = teacher.full_name
                        messages.success(request, f'Welcome, {teacher.full_name}!')
                        return redirect('teacher_dashboard')
                    else:
                        messages.error(request, 'Invalid password!')
                except Teacher.DoesNotExist:
                    messages.error(request, 'Teacher not found!')
                    
            elif role == 'student':
                try:
                    student = Student.objects.get(username=username)
                    if student.check_password(password):
                        request.session['user_id'] = student.id
                        request.session['user_role'] = 'student'
                        request.session['user_name'] = student.full_name
                        messages.success(request, f'Welcome, {student.full_name}!')
                        return redirect('student_dashboard')
                    else:
                        messages.error(request, 'Invalid password!')
                except Student.DoesNotExist:
                    messages.error(request, 'Student not found!')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Logout view"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


# ==================== ADMIN DASHBOARD ====================

def admin_required(view_func):
    """Decorator to check if user is admin - auto-login if not logged in"""
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_role') != 'admin':
            # Auto-login as admin for direct access
            try:
                admin = Admin.objects.first()
                if admin:
                    request.session['user_id'] = admin.id
                    request.session['user_role'] = 'admin'
                    request.session['user_name'] = admin.full_name
            except:
                messages.error(request, 'Admin not found.')
                return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    """Admin dashboard view"""
    context = {
        'total_teachers': Teacher.objects.count(),
        'total_students': Student.objects.count(),
        'total_classes': Class.objects.count(),
        'total_subjects': Subject.objects.count(),
        'recent_students': Student.objects.order_by('-created_at')[:5],
        'recent_teachers': Teacher.objects.order_by('-created_at')[:5],
        'user_name': request.session.get('user_name', 'Admin'),
    }
    return render(request, 'admin/dashboard.html', context)


# ==================== STUDENT MANAGEMENT ====================

@admin_required
def student_list(request):
    """View all students"""
    students = Student.objects.all().order_by('-created_at')
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    return render(request, 'admin/students/list.html', {'students': students})


@admin_required
def student_add(request):
    """Add new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            password = request.POST.get('password')
            if password:
                student.set_password(password)
            student.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'admin/students/form.html', {'form': form, 'title': 'Add Student'})


@admin_required
def student_edit(request, pk):
    """Edit student"""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            password = request.POST.get('password')
            if password:
                student.set_password(password)
            student.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'admin/students/form.html', {'form': form, 'title': 'Edit Student', 'student': student})


@admin_required
def student_detail(request, pk):
    """View student details"""
    student = get_object_or_404(Student, pk=pk)
    attendances = StudentAttendance.objects.filter(student=student).order_by('-date')[:30]
    fees = Fees.objects.filter(student=student).order_by('-created_at')
    return render(request, 'admin/students/detail.html', {
        'student': student,
        'attendances': attendances,
        'fees': fees
    })


@admin_required
def student_delete(request, pk):
    """Delete student"""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'admin/students/delete.html', {'student': student})


# ==================== TEACHER MANAGEMENT ====================

@admin_required
def teacher_list(request):
    """View all teachers"""
    teachers = Teacher.objects.all().order_by('-created_at')
    paginator = Paginator(teachers, 10)
    page = request.GET.get('page')
    teachers = paginator.get_page(page)
    return render(request, 'admin/teachers/list.html', {'teachers': teachers})


@admin_required
def teacher_add(request):
    """Add new teacher"""
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            password = request.POST.get('password')
            if password:
                teacher.set_password(password)
            teacher.save()
            messages.success(request, 'Teacher added successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'admin/teachers/form.html', {'form': form, 'title': 'Add Teacher'})


@admin_required
def teacher_edit(request, pk):
    """Edit teacher"""
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            teacher = form.save(commit=False)
            password = request.POST.get('password')
            if password:
                teacher.set_password(password)
            teacher.save()
            messages.success(request, 'Teacher updated successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'admin/teachers/form.html', {'form': form, 'title': 'Edit Teacher', 'teacher': teacher})


@admin_required
def teacher_detail(request, pk):
    """View teacher details"""
    teacher = get_object_or_404(Teacher, pk=pk)
    attendances = TeacherAttendance.objects.filter(teacher=teacher).order_by('-date')[:30]
    salaries = Salary.objects.filter(teacher=teacher).order_by('-created_at')
    return render(request, 'admin/teachers/detail.html', {
        'teacher': teacher,
        'attendances': attendances,
        'salaries': salaries
    })


@admin_required
def teacher_delete(request, pk):
    """Delete teacher"""
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teacher_list')
    return render(request, 'admin/teachers/delete.html', {'teacher': teacher})


# ==================== CLASS MANAGEMENT ====================

@admin_required
def class_list(request):
    """View all classes"""
    classes = Class.objects.all().annotate(student_count=Count('students')).order_by('name')
    return render(request, 'admin/classes/list.html', {'classes': classes})


@admin_required
def class_add(request):
    """Add new class"""
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class added successfully!')
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'admin/classes/form.html', {'form': form, 'title': 'Add Class'})


@admin_required
def class_edit(request, pk):
    """Edit class"""
    cls = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully!')
            return redirect('class_list')
    else:
        form = ClassForm(instance=cls)
    return render(request, 'admin/classes/form.html', {'form': form, 'title': 'Edit Class'})


@admin_required
def class_delete(request, pk):
    """Delete class"""
    cls = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        cls.delete()
        messages.success(request, 'Class deleted successfully!')
        return redirect('class_list')
    return render(request, 'admin/classes/delete.html', {'class': cls})


# ==================== SUBJECT MANAGEMENT ====================

@admin_required
def subject_list(request):
    """View all subjects"""
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'admin/subjects/list.html', {'subjects': subjects})


@admin_required
def subject_add(request):
    """Add new subject"""
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully!')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'admin/subjects/form.html', {'form': form, 'title': 'Add Subject'})


@admin_required
def subject_edit(request, pk):
    """Edit subject"""
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'admin/subjects/form.html', {'form': form, 'title': 'Edit Subject'})


@admin_required
def subject_delete(request, pk):
    """Delete subject"""
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('subject_list')
    return render(request, 'admin/subjects/delete.html', {'subject': subject})


# ==================== ATTENDANCE MANAGEMENT ====================

@admin_required
def student_attendance_list(request):
    """View student attendance"""
    selected_date = request.GET.get('date', date.today().isoformat())
    selected_class = request.GET.get('class', '')
    
    attendances = StudentAttendance.objects.filter(date=selected_date)
    if selected_class:
        attendances = attendances.filter(student__student_class_id=selected_class)
    
    classes = Class.objects.all()
    return render(request, 'admin/attendance/student_list.html', {
        'attendances': attendances,
        'classes': classes,
        'selected_date': selected_date,
        'selected_class': selected_class
    })


@admin_required
def student_attendance_mark(request):
    """Mark student attendance"""
    selected_date = request.GET.get('date', date.today().isoformat())
    selected_class = request.GET.get('class', '')
    
    if request.method == 'POST':
        attendance_date = request.POST.get('date')
        for key, value in request.POST.items():
            if key.startswith('status_'):
                student_id = key.replace('status_', '')
                StudentAttendance.objects.update_or_create(
                    student_id=student_id,
                    date=attendance_date,
                    defaults={'status': value}
                )
        messages.success(request, 'Attendance marked successfully!')
        return redirect('student_attendance_list')
    
    students = Student.objects.all()
    if selected_class:
        students = students.filter(student_class_id=selected_class)
    
    classes = Class.objects.all()
    return render(request, 'admin/attendance/student_mark.html', {
        'students': students,
        'classes': classes,
        'selected_date': selected_date,
        'selected_class': selected_class
    })


@admin_required
def teacher_attendance_list(request):
    """View teacher attendance"""
    selected_date = request.GET.get('date', date.today().isoformat())
    attendances = TeacherAttendance.objects.filter(date=selected_date)
    return render(request, 'admin/attendance/teacher_list.html', {
        'attendances': attendances,
        'selected_date': selected_date
    })


@admin_required
def teacher_attendance_mark(request):
    """Mark teacher attendance"""
    selected_date = request.GET.get('date', date.today().isoformat())
    
    if request.method == 'POST':
        attendance_date = request.POST.get('date')
        for key, value in request.POST.items():
            if key.startswith('status_'):
                teacher_id = key.replace('status_', '')
                TeacherAttendance.objects.update_or_create(
                    teacher_id=teacher_id,
                    date=attendance_date,
                    defaults={'status': value}
                )
        messages.success(request, 'Teacher attendance marked successfully!')
        return redirect('teacher_attendance_list')
    
    teachers = Teacher.objects.all()
    return render(request, 'admin/attendance/teacher_mark.html', {
        'teachers': teachers,
        'selected_date': selected_date
    })


# ==================== FEES MANAGEMENT ====================

@admin_required
def fees_list(request):
    """View all fees"""
    fees = Fees.objects.all().order_by('-created_at')
    paginator = Paginator(fees, 10)
    page = request.GET.get('page')
    fees = paginator.get_page(page)
    return render(request, 'admin/fees/list.html', {'fees': fees})


@admin_required
def fees_add(request):
    """Add new fee"""
    if request.method == 'POST':
        form = FeesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee added successfully!')
            return redirect('fees_list')
    else:
        form = FeesForm()
    return render(request, 'admin/fees/form.html', {'form': form, 'title': 'Add Fee'})


@admin_required
def fees_edit(request, pk):
    """Edit fee"""
    fee = get_object_or_404(Fees, pk=pk)
    if request.method == 'POST':
        form = FeesForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee updated successfully!')
            return redirect('fees_list')
    else:
        form = FeesForm(instance=fee)
    return render(request, 'admin/fees/form.html', {'form': form, 'title': 'Edit Fee'})


@admin_required
def fees_delete(request, pk):
    """Delete fee"""
    fee = get_object_or_404(Fees, pk=pk)
    if request.method == 'POST':
        fee.delete()
        messages.success(request, 'Fee deleted successfully!')
        return redirect('fees_list')
    return render(request, 'admin/fees/delete.html', {'fee': fee})


# ==================== SALARY MANAGEMENT ====================

@admin_required
def salary_list(request):
    """View all salaries"""
    salaries = Salary.objects.all().order_by('-created_at')
    paginator = Paginator(salaries, 10)
    page = request.GET.get('page')
    salaries = paginator.get_page(page)
    return render(request, 'admin/salary/list.html', {'salaries': salaries})


@admin_required
def salary_add(request):
    """Add new salary"""
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salary added successfully!')
            return redirect('salary_list')
    else:
        form = SalaryForm()
    return render(request, 'admin/salary/form.html', {'form': form, 'title': 'Add Salary'})


@admin_required
def salary_edit(request, pk):
    """Edit salary"""
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salary updated successfully!')
            return redirect('salary_list')
    else:
        form = SalaryForm(instance=salary)
    return render(request, 'admin/salary/form.html', {'form': form, 'title': 'Edit Salary'})


@admin_required
def salary_delete(request, pk):
    """Delete salary"""
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        salary.delete()
        messages.success(request, 'Salary deleted successfully!')
        return redirect('salary_list')
    return render(request, 'admin/salary/delete.html', {'salary': salary})


# ==================== TEACHER DASHBOARD ====================

def teacher_required(view_func):
    """Decorator to check if user is teacher"""
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_role') != 'teacher':
            messages.error(request, 'You must be logged in as teacher to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@teacher_required
def teacher_dashboard(request):
    """Teacher dashboard view"""
    teacher_id = request.session.get('user_id')
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    
    # Get attendance stats
    today = date.today()
    month_start = today.replace(day=1)
    
    monthly_attendance = TeacherAttendance.objects.filter(
        teacher=teacher,
        date__gte=month_start,
        date__lte=today
    )
    
    present_count = monthly_attendance.filter(status='present').count()
    absent_count = monthly_attendance.filter(status='absent').count()
    late_count = monthly_attendance.filter(status='late').count()
    
    context = {
        'teacher': teacher,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'recent_attendance': TeacherAttendance.objects.filter(teacher=teacher).order_by('-date')[:10],
        'user_name': request.session.get('user_name', 'Teacher'),
    }
    return render(request, 'teacher/dashboard.html', context)


@teacher_required
def teacher_attendance_history(request):
    """View teacher's own attendance history"""
    teacher_id = request.session.get('user_id')
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    
    month = request.GET.get('month', date.today().strftime('%Y-%m'))
    year, month_num = map(int, month.split('-'))
    
    attendances = TeacherAttendance.objects.filter(
        teacher=teacher,
        date__year=year,
        date__month=month_num
    ).order_by('date')
    
    return render(request, 'teacher/attendance_history.html', {
        'teacher': teacher,
        'attendances': attendances,
        'selected_month': month
    })


@teacher_required
def teacher_mark_student_attendance(request):
    """Teacher marks student attendance"""
    selected_date = request.GET.get('date', date.today().isoformat())
    selected_class = request.GET.get('class', '')
    
    teacher_id = request.session.get('user_id')
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    
    if request.method == 'POST':
        attendance_date = request.POST.get('date')
        for key, value in request.POST.items():
            if key.startswith('status_'):
                student_id = key.replace('status_', '')
                StudentAttendance.objects.update_or_create(
                    student_id=student_id,
                    date=attendance_date,
                    defaults={'status': value, 'marked_by': teacher}
                )
        messages.success(request, 'Student attendance marked successfully!')
        return redirect('teacher_mark_student_attendance')
    
    students = Student.objects.all()
    if selected_class:
        students = students.filter(student_class_id=selected_class)
    
    classes = Class.objects.all()
    return render(request, 'teacher/mark_attendance.html', {
        'students': students,
        'classes': classes,
        'selected_date': selected_date,
        'selected_class': selected_class
    })


# ==================== STUDENT DASHBOARD ====================

def student_required(view_func):
    """Decorator to check if user is student"""
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_role') != 'student':
            messages.error(request, 'You must be logged in as student to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@student_required
def student_dashboard(request):
    """Student dashboard view"""
    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, pk=student_id)
    
    # Get attendance stats
    today = date.today()
    month_start = today.replace(day=1)
    
    monthly_attendance = StudentAttendance.objects.filter(
        student=student,
        date__gte=month_start,
        date__lte=today
    )
    
    present_count = monthly_attendance.filter(status='present').count()
    absent_count = monthly_attendance.filter(status='absent').count()
    late_count = monthly_attendance.filter(status='late').count()
    
    # Get fees
    pending_fees = Fees.objects.filter(student=student, status='unpaid')
    
    context = {
        'student': student,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'recent_attendance': StudentAttendance.objects.filter(student=student).order_by('-date')[:10],
        'pending_fees': pending_fees,
        'user_name': request.session.get('user_name', 'Student'),
    }
    return render(request, 'student/dashboard.html', context)


@student_required
def student_attendance_history(request):
    """View student's own attendance history"""
    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, pk=student_id)
    
    month = request.GET.get('month', date.today().strftime('%Y-%m'))
    year, month_num = map(int, month.split('-'))
    
    attendances = StudentAttendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month_num
    ).order_by('date')
    
    return render(request, 'student/attendance_history.html', {
        'student': student,
        'attendances': attendances,
        'selected_month': month
    })


@student_required
def student_fees_history(request):
    """View student's fees history"""
    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, pk=student_id)
    
    fees = Fees.objects.filter(student=student).order_by('-created_at')
    
    return render(request, 'student/fees_history.html', {
        'student': student,
        'fees': fees
    })
