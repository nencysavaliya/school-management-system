from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin Dashboard
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    
    # Student Management
    path('admin-panel/students/', views.student_list, name='student_list'),
    path('admin-panel/students/add/', views.student_add, name='student_add'),
    path('admin-panel/students/<int:pk>/', views.student_detail, name='student_detail'),
    path('admin-panel/students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('admin-panel/students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Teacher Management
    path('admin-panel/teachers/', views.teacher_list, name='teacher_list'),
    path('admin-panel/teachers/add/', views.teacher_add, name='teacher_add'),
    path('admin-panel/teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('admin-panel/teachers/<int:pk>/edit/', views.teacher_edit, name='teacher_edit'),
    path('admin-panel/teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
    
    # Class Management
    path('admin-panel/classes/', views.class_list, name='class_list'),
    path('admin-panel/classes/add/', views.class_add, name='class_add'),
    path('admin-panel/classes/<int:pk>/edit/', views.class_edit, name='class_edit'),
    path('admin-panel/classes/<int:pk>/delete/', views.class_delete, name='class_delete'),
    
    # Subject Management
    path('admin-panel/subjects/', views.subject_list, name='subject_list'),
    path('admin-panel/subjects/add/', views.subject_add, name='subject_add'),
    path('admin-panel/subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    path('admin-panel/subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
    
    # Student Attendance
    path('admin-panel/attendance/students/', views.student_attendance_list, name='student_attendance_list'),
    path('admin-panel/attendance/students/mark/', views.student_attendance_mark, name='student_attendance_mark'),
    
    # Teacher Attendance
    path('admin-panel/attendance/teachers/', views.teacher_attendance_list, name='teacher_attendance_list'),
    path('admin-panel/attendance/teachers/mark/', views.teacher_attendance_mark, name='teacher_attendance_mark'),
    
    # Fees Management
    path('admin-panel/fees/', views.fees_list, name='fees_list'),
    path('admin-panel/fees/add/', views.fees_add, name='fees_add'),
    path('admin-panel/fees/<int:pk>/edit/', views.fees_edit, name='fees_edit'),
    path('admin-panel/fees/<int:pk>/delete/', views.fees_delete, name='fees_delete'),
    
    # Salary Management
    path('admin-panel/salary/', views.salary_list, name='salary_list'),
    path('admin-panel/salary/add/', views.salary_add, name='salary_add'),
    path('admin-panel/salary/<int:pk>/edit/', views.salary_edit, name='salary_edit'),
    path('admin-panel/salary/<int:pk>/delete/', views.salary_delete, name='salary_delete'),
    
    # Teacher Dashboard
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/attendance/', views.teacher_attendance_history, name='teacher_attendance_history'),
    path('teacher/mark-attendance/', views.teacher_mark_student_attendance, name='teacher_mark_student_attendance'),
    
    # Student Dashboard
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/attendance/', views.student_attendance_history, name='student_attendance_history'),
    path('student/fees/', views.student_fees_history, name='student_fees_history'),
]
