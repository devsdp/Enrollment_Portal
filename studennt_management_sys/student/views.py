from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from rest_framework import viewsets
from .serializers import StateSerializer, DistrictSerializer, BlockSerializer, VillageSerializer, ProgramSerializer, StudentSerializer
from .models import State, District, Block, Village, Program, Student
import io
import csv
from django.db.models import Count
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Student
from django.contrib import messages
from reportlab.pdfgen import canvas
from io import BytesIO
from django import forms
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.core.paginator import Paginator
from django.http import HttpResponse
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph



@login_required(login_url='login/')
def HomePage(request):
    context = {'username': request.user.username}
    return render (request,'student/home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirmed password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'student/signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("USERNAME OR PASSWORD IS INCORRECT!!!")

    return render (request,'student/login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login/')
def state_list(request):
    states_list = State.objects.all()
    paginator = Paginator(states_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student/state_list.html', {'page_obj': page_obj})
@login_required(login_url='login/')
def state_detail(request, pk):
    state = get_object_or_404(State, pk=pk)
    districts = District.objects.filter(state=state)
    return render(request, 'student/state_detail.html', {'state': state, 'districts': districts})

@login_required(login_url='login/')
def district_list(request):
    district_list = District.objects.order_by('name')
    paginator = Paginator(district_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student/district_list.html', {'page_obj': page_obj})
@login_required(login_url='login/')
def district_detail(request, pk):
    district = get_object_or_404(District, pk=pk)
    blocks = Block.objects.filter(district=district)
    return render(request, 'student/district_detail.html', {'district': district, 'blocks': blocks})

@login_required(login_url='login/')
def block_list(request):
    block_list = Block.objects.order_by('name')
    paginator = Paginator(block_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student/block_list.html', {'page_obj': page_obj})
@login_required(login_url='login/')
def block_detail(request, pk):
    block = get_object_or_404(Block, pk=pk)
    villages = Village.objects.filter(block=block)
    context = {'block': block, 'villages': villages}
    return render(request, 'student/block_detail.html', context)

@login_required(login_url='login/')
def village_list(request):
    villages = Village.objects.order_by('name')
    paginator = Paginator(villages, 10)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/village_list.html', {'page_obj': page_obj})
@login_required(login_url='login/')
def village_detail(request, pk):
    village = get_object_or_404(Village, pk=pk)
    students = Student.objects.filter(village=village)
    return render(request, 'student/village_detail.html', {'village': village, 'students': students})

@login_required(login_url='login/')
def program_list(request):
    programs = Program.objects.all()
    return render(request, 'student/program_list.html', {'programs': programs})
@login_required(login_url='login/')
def program_detail(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    students = Student.objects.filter(program=program).order_by('first_name')
    return render(request, 'student/program_detail.html', {'program': program, 'students': students})

def student_list(request):
    students = Student.objects.all().values('id', 'first_name', 'last_name', 'program', 'block', 'village', 'district', 'state', 'enrollment_number', 'email', 'phone')
    program_counts = Student.objects.values('program').annotate(count=Count('program'))
    village_counts = Student.objects.values('village').annotate(count=Count('village'))
    block_counts = Student.objects.values('block').annotate(count=Count('block'))
    district_counts = Student.objects.values('district').annotate(count=Count('district'))
    state_counts = Student.objects.values('state').annotate(count=Count('state'))
    context = {
        'students': students,
        'program_counts': program_counts,
        'village_counts': village_counts,
        'block_counts': block_counts,
        'district_counts': district_counts,
        'state_counts': state_counts,
    }
    return render(request, 'student/student_list.html', context)



@login_required(login_url='login/')
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student/student_detail.html', {'student': student})

    
@login_required(login_url='login/')
def dashboard(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'dashboard.html', context)

@login_required(login_url='login/')
def state_dashboard(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'student/state_dashboard.html', context)

@login_required(login_url='login/')
@login_required(login_url='block_login')
def block_dashboard(request):
    students = Student.objects.all()
    context = {'students' : students}
    return render(request, 'block_dashboard.html',context)



class StudentForm(forms.ModelForm):
    village = forms.ModelChoiceField(queryset=Village.objects.all())
    block = forms.ModelChoiceField(queryset=Block.objects.all())
    district = forms.ModelChoiceField(queryset=District.objects.all())
    state = forms.ModelChoiceField(queryset=State.objects.all())
    program = forms.ModelChoiceField(queryset=Program.objects.all())
    enrollment_number = forms.IntegerField(initial=0, widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'enrollment_number', 'village', 'program', 'block', 'district', 'state')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['village'].empty_label = "Select Village"
        self.fields['block'].empty_label = "Select Block"
        self.fields['district'].empty_label = "Select District"
        self.fields['state'].empty_label = "Select State"
        self.fields['program'].empty_label = "Select Program"

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        village = cleaned_data.get('village')
        block = cleaned_data.get('block')
        district = cleaned_data.get('district')
        state = cleaned_data.get('state')
        program = cleaned_data.get('program')

        cleaned_data['first_name'] = first_name.upper()
        cleaned_data['last_name'] = last_name.upper()

        return cleaned_data


@login_required(login_url='block-login')
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.enrollment_number = 0
            student.save()
            return redirect('block_dashboard')
    else:
        form = StudentForm()
    context = {'form': form}
    return render(request, 'student/add_student.html', context)

@login_required(login_url='/login/')
def edit_student(request, id):
    student = get_object_or_404(Student, pk=id)
    if request.method == 'POST':
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.village = request.POST['village']
        student.program = request.POST['program']
        student.block = request.POST['block']
        student.district = request.POST['district']
        student.state = request.POST['state']
        student.save()
        messages.success(request, f'{student.first_name} {student.last_name} updated successfully.')
        return redirect('block_dashboard')

    villages = Village.objects.all()
    programs = Program.objects.all()
    blocks = Block.objects.all()
    districts = District.objects.all()
    states = State.objects.all()
    context = {
        'student': student,
        'villages': villages,
        'programs': programs,
        'blocks': blocks,
        'districts': districts,
        'states': states,
    }
    return render(request, 'student/edit_student.html', context)

@login_required(login_url='/login/')
def delete_student(request, id):
    student = get_object_or_404(Student, pk=id)
    student.delete()
    messages.success(request, f'{student.first_name} deleted successfully.')
    return redirect('block_dashboard')



#for csv file
@login_required(login_url='login/')
def download_students(request):
    if request.method == 'POST':
        state = request.POST.get('states')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{state} STUDENTS DATA.CSV"'
        writer = csv.writer(response)
        writer.writerow(['First_Name','Last_Name','Enroll_Num','Program','Village','Block','District','State'])

        if state:
            students = Student.objects.filter(state=state)
        else:
            students = Student.objects.all()

        for student in students:
            first_name, last_name = student.first_name,student.last_name
            writer.writerow([first_name, last_name,student.enrollment_number,student.program,student.village,student.block,student.district,student.state])

        return response
    else:
        states = Student.objects.values_list('state', flat=True).distinct()
        return render(request, 'csv.html', {'states': states})


#for specific state
@login_required(login_url='login/')
def generate_pdf(request):
    if request.method == 'POST':
        selected_state = request.POST.get('states')
        if selected_state:
            students = Student.objects.filter(state=selected_state)
        else:
            students = Student.objects.all()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{selected_state} STUDENTS DATA.PDF"'


        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()

        table_width, table_height = letter
        col_widths = [table_width * 0.13, table_width * 0.12, table_width * 0.07, table_width * 0.10, table_width * 0.12, table_width * 0.12, table_width * 0.12, table_width * 0.20]

        table_data = [['First_Name','Last_Name','Enroll','Program','Village','Block','District','State']]

        for student in students:
            table_data.append([student.first_name, student.last_name, student.enrollment_number, student.program, student.village, student.block, student.district, student.state])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        student_table = Table(table_data, colWidths=col_widths)
        student_table.setStyle(table_style)

        doc.build([student_table])

        return response

    else:
        states = Student.objects.values_list('state', flat=True).distinct().order_by('state')
        return render(request, 'generate_pdf.html', {'states': states})


#for specific program
def download_pdf(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    students = Student.objects.filter(program=program)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=" {program} STUDENTS DATA.PDF"'


    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    table_width, table_height = letter
    col_widths = [table_width * 0.13, table_width * 0.12, table_width * 0.07, table_width * 0.10, table_width * 0.12, table_width * 0.12, table_width * 0.12, table_width * 0.20]

    table_data = [['First_Name','Last_Name','Enroll','Program','Village','Block','District','State']]

    for student in students:
        table_data.append([student.first_name, student.last_name, student.enrollment_number, student.program, student.village, student.block, student.district, student.state])

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0,0),(-1,-1), 1, colors.black)
    ])

    student_table = Table(table_data, colWidths=col_widths)
    student_table.setStyle(table_style)

    elements = []
    elements.append(Paragraph(f'<strong>{program.name} STUDENTS LIST</strong>', styles['Heading1']))
    elements.append(Paragraph(f'<br/><br/>', styles['Normal']))
    elements.append(student_table)
    doc.build(elements)

    return response


#for uploading csv file
@login_required(login_url='login/')
def upload(request):
    if request.method == "POST":
        csv_file = request.FILES["myfile"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return redirect('upload')

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Student.objects.update_or_create(
                first_name=column[0],
                last_name=column[1],
                enrollment_number=column[2],
                program=column[3],
                village=column[4],
                block=column[5],
                district=column[6],
                state=column[7],
                
            )
        messages.success(request, "YOUR FILE HAS BEEN UPLOADED SUCCESSFULLY AND THE DATA HAS BEEN SAVED TO THE DATABASE.")
        return redirect('success')

    return render(request, 'upload.html')

#for successful upload of csv file
@login_required(login_url='login/')
def success(request):
    students = Student.objects.all()
    return render(request, 'success.html', {'students': students})
