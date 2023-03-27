from django.urls import path
from . import views
from .views import state_dashboard, download_students, dashboard
from .views import generate_pdf
from .views import  upload


app_name = 'student'

urlpatterns = [
    path('states/', views.state_list, name='state_list'),
    path('states/<int:pk>/', views.state_detail, name='state_detail'),
    path('districts/', views.district_list, name='district_list'),
    path('districts/<int:pk>/', views.district_detail, name='district_detail'),
    path('blocks/', views.block_list, name='block_list'),
    path('blocks/<int:pk>/', views.block_detail, name='block_detail'),
    path('villages/', views.village_list, name='village_list'),
    path('villages/<int:pk>/', views.village_detail, name='village_detail'),
    path('programs/', views.program_list, name='program_list'),
    path('program/<int:program_id>/', views.program_detail, name='program_detail'),
    path('students/', views.student_list, name='student_list'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('dashboard/', dashboard, name='dashboard'),
    path('download_students/',views.download_students, name='csvs'),
    path('download_pdf/', views.generate_pdf, name='download_pdf'),
    path('generte_pdf/', views.generate_pdf, name='download'),
    path('edit_student/', views.edit_student, name='edit_student'),
    path('delete_student/', views.delete_student, name='delete_student'),
]



    



