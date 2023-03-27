"""studennt_management_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from block_auth.views import BlockLoginView
from django.contrib import admin
from django.urls import  include,path
from django.contrib.auth import views as auth_views
from student import views
from student.views import upload,success
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.SignupPage,name='signup'),
    path('', views.LoginPage, name='login'),
    path('home/',views.HomePage,name='home'),
    path('student/',include('student.urls')),
    path('logout/',views.LogoutPage,name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('state_dashboard/', views.state_dashboard, name='state_dashboard'),
    path('block_dashboard/', views.block_dashboard, name='block_dashboard'),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('students/', views.student_list, name='student_list'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('download_students/',views.download_students, name='csvs'),
    path('upload/', views.upload, name='upload'),
    path('generte_pdf/', views.generate_pdf, name='download'),
    path('downloadpdf/<int:program_id>/', views.download_pdf, name='downloadpdf'),
    path('success/', views.success, name='success'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('block-login/', BlockLoginView.as_view(), name='block_login'),

]

