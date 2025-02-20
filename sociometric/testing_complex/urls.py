from django.urls import path
from django.contrib import admin
from . import views



urlpatterns = [
    path('', views.user_login, name='login'),

    path('home', views.home, name='home'),

    path('logout', views.log_out, name='logout'),

    path('home/add_student', views.add_student, name='add_student'),
    path('home/sociyounger', views.sociyounger, name='sociyounger'),
    path('home/sociolder', views.sociolder, name='sociolder'),
    path('home/test_link/<str:data>', views.test_link, name='test_link'),

    path('home/class/<str:data>', views.class_info, name='class_info'),
    path('home/class/student_info/<str:data>', views.student_info, name='student_info'),
    path('home/class/class_soci_info/<str:data>', views.class_soci_info, name='class_soci_info'),

    path('student/login/<str:data>', views.student_login, name='student_login'),
    path('student/test/<str:data>', views.student_test, name='student_test'),
]
