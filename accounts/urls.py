from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('unauthorized/', unauthorized_view, name='unauthorized'),
    path('student/info/', student_info_view, name='student_info'),
    path('teacher/info/', teacher_info_view, name='teacher_info'),
    path('teacher/timetable/', teacher_timetable_view, name='teacher_timetable'),
    path('admin/class/add/', class_add_view, name='class_add'),
    path('admin/class/list/', class_list_view, name='class_list'),
    path('teacher/add-marks/', add_student_marks, name='add_marks'),
    path('student/marks/', student_marks_view, name='student_marks'),
    path('teacher/send-notice/', send_notice_view, name='send_notice'),
    path('student/notices/', student_notices_view, name='student_notices'),
    path('admin/general-notice/', send_general_notice, name='send_general_notice'),
    path('user/general-notices/', general_notices_view, name='general_notices'),
     path('teacher/attendance/', take_attendance_view, name='take_attendance'),
]
