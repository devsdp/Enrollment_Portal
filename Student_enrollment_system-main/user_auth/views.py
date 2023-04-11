import json
import requests
import time
from django.contrib.auth import  logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import render , redirect
from .models import CustomUser , Students , State , Block
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




class Userlogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.user_type == '1':_type = 'AdminHod'
        elif user.user_type == '2':_type = 'state'
        elif user.user_type == '3':_type = 'block'
        elif user.user_type == '4':_type = 'student'
        else: _type=None
        # print(created)
        context = {
            "user_id":user.id,
            "user_email":user.email,
            "user_type":user.user_type,
            "msg" : _type,
            "token":token.key,
            }
        return Response(context)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    request.user.auth_token.delete()
    return redirect("/login_user")



def adminhome_dashboard(request):
    state = State.objects.all()
    print("the state ************",state)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(state, 10)

    try:        
        state_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        state_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        state_data = paginator.page(paginator.num_pages)

    blocks_data = Block.objects.all()
    paginator = Paginator(blocks_data, 10)
    page = request.GET.get('block_page',1)
    try:
        blocks_data = paginator.page(page)
    except PageNotAnInteger:
        blocks_data = paginator.page(1)
    except EmptyPage:
        blocks_data = paginator.page(paginator.num_pages)

    user_data = CustomUser.objects.all()
    paginator = Paginator(user_data, 10)
    page = request.GET.get('user_page',1)
    try:
        user_data = paginator.page(page)
    except PageNotAnInteger:
        user_data = paginator.page(1)
    except EmptyPage:
        user_data = paginator.page(paginator.num_pages)

    context ={
        "state":state_data,
        "blocks":blocks_data,
        "user":user_data,

    }
    return render(request, "Student_template/admin_dashboard.html",context)




def block_create(request):
    return render(request, "Student_template/block_create.html")

def block_dasboard(request):
    return render(request, "Student_template/block_dashboard.html")

def login(request):
    return render(request, "Student_template/login.html")

def program(request):
    return render(request, "Student_template/program.html")

def state_allocation(request):
    return render(request, "Student_template/state_allocation.html")

def state_create(request):
    return render(request, "Student_template/state_create.html")

def state_dasboard(request):
    return render(request, "Student_template/state_dashboard.html")

def user_creat(request):
    return render(request, "Student_template/create_users.html")

def village(request):
    return render(request, "Student_template/village.html")
  

def block_allocation(request):
    return render(request, "Student_template/block_allocate.html")

def group_view(request):
    return render(request, "Student_template/group_view.html")

def State_Students_view(request):
    return render(request, "Student_template/state_student_view.html")

def mentor_create(request):
    return render(request, "Student_template/mentor_create.html")

def block_user(request):
    return render(request, "Student_template/block_user.html")

def all_user_view(request):

    user = CustomUser.objects.all()

    context={
        "custom_user" :user
    }

    return render(request, "Student_template/all_users.html",context)


def block_student_view(request):
    return render(request, "Student_template/block_student_view.html")

def program_student_view(request):
    return render(request, "Student_template/program_student_view.html")

def village_student_view(request):
    return render(request, "Student_template/village_student_view.html")


def student_view_data(request):
    

    students_data_inactive = Students.objects.all().filter(status=False)
    students_data_active = Students.objects.all().filter(status=True)

    context = {
        "inactaive_students" : students_data_inactive,
        "active_students": students_data_active
    }
    return render(request, "Student_template/students.html", context)


def results(request):

    state_id = request.POST.get('state')
    district_id = request.POST.get('district')
    block_id = request.POST.get('block')
    village_id = request.POST.get('village')

    students_data_inactive = Students.objects.all().filter(status=False)

    if state_id is not None:
        students_data_inactive = students_data_inactive.filter(state_id=state_id)

    if district_id is not None:
        students_data_inactive = students_data_inactive.filter(district_id=district_id)

    if block_id is not None:
        students_data_inactive = students_data_inactive.filter(block_id=block_id)

    if village_id is not None:
        students_data_inactive = students_data_inactive.filter(village_id=village_id)

    students_data_active = Students.objects.all().filter(status=True)
    context = {
        "inactaive_students" : students_data_inactive,
        "active_students": students_data_active
    }
    return render(request, "Student_template/students.html", context)
    
    

def toggle(request):
    w = Students.objects.get(id=request.POST['id'])
    w.status = request.POST['status'] == True
    w.save()
    return HttpResponse('success')

from django.shortcuts import get_object_or_404

def student_detail(request, id):
    print("the studenet", id)
    student = get_object_or_404(Students, id=id)
    if request.method == 'POST':
        if request.POST.get('action') == 'toggle_active':
            student.status = not student.status
            student.save()
            return redirect('/student_view_data')
        elif request.POST.get('action') == 'toggle_inactive':
            student.status =not student.status
            student.save()
            return redirect('/student_view_data')
        


def multiple_student_update(request):
    print("the student")
    selected_options = request.POST.get('selection')
    print("the datais ",selected_options)
    selected_checklits = request.POST.getlist('filetouse')
    print("the datais ",selected_checklits)
    selected_check_active = request.POST.getlist('activestudent')
    if selected_options == "Active selected Student":
        for i in selected_checklits:
            print("hello")
            student = get_object_or_404(Students, enrollment_id=i)
            student.status =not student.status
            student.save()
    elif selected_options=="Delete Selected":
        for i in selected_checklits:
            student = get_object_or_404(Students, enrollment_id=i)
            student.delete()
    elif selected_options=="DeActive Selected":
        for i in selected_check_active:
            student = get_object_or_404(Students, enrollment_id=i)
            student.status =not student.status
            student.save()

    return redirect('/student_view_data')


# def logout_request(request):
#     logout(request)
#     return redirect("/login_user")

#new code
from .models import District
def state_login_admin(request):
    url = "http://127.0.0.1:8000/login/"
    payload = json.dumps({
        "username": "admin",
        "password": "123456"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response_login = requests.post(url, headers=headers, data=payload)
    login_details = json.loads(response_login.text)
    print("Token:", login_details['token'])
    token = login_details['token']

    while True:
        url = "https://prathamyouthnet.org/apis/enrollment-id/dbfetch-states.php?token=eyNsWgAdBF0KafwGP?wOCRVn-tJE=zlc9v-=-9h5rHeh?ZTB?uAKYxDxv8zRgJy?uP-Kn?57kT?3Kp!202RROdY!a1XRy3UVc5S/UPzG4zCsUbT-Pr3nnuW0fhCTp93L"
        response = requests.get(url)
        data = json.loads(response.text)

        if data[0]['is_error'] == '0':
            for item in data[1:]:
                state_name = item['StateName']
                if State.objects.filter(name=state_name).exists():
                    print("State already exists:", state_name)
                    continue
                
                else:
                    state_name = item['StateName']
                    url = "http://127.0.0.1:8000/state_create/"
                    payload = json.dumps({
                        "name": state_name,
                    })
                    headers = {
                        'Authorization': 'token ' + login_details['token'],
                        'Content-Type': 'application/json'  
                    }
                    response_state = requests.post(url, headers=headers, data=payload.encode('utf-8'))
                    print(response_state.text)
                

                # Get district data from external API
                url = f"https://prathamyouthnet.org/apis/enrollment-id/dbfetch-state-districts.php?state={state_name}&&token=eyNsWgAdBF0KafwGP?wOCRVn-tJE=zlc9v-=-9h5rHeh?ZTB?uAKYxDxv8zRgJy?uP-Kn?57kT?3Kp!202RROdY!a1XRy3UVc5S/UPzG4zCsUbT-Pr3nnuW0fhCTp93L"
                response = requests.get(url)
                district_data = json.loads(response.text)

                if district_data[0]['is_error'] == '0':
                    for district_item in district_data[1:]:
                        district_name = district_item['DistrictName']

                        state = State.objects.filter(name=state_name).first()

                        if state:
                            url = "http://127.0.0.1:8000/create_district/"
                            payload = json.dumps({
                                "name": district_name,
                                "state": state.pk
                            })
                            headers = {
                                'Authorization': 'token ' + token,
                                'Content-Type': 'application/json'  
                            }
                            response_district = requests.post(url, headers=headers, data=payload)
                            print(response_district.text)

                            url = f"https://prathamyouthnet.org/apis/enrollment-id/dbfetch-state-district-blocks.php?state={state_name}&&district={district_name}&&token=eyNsWgAdBF0KafwGP?wOCRVn-tJE=zlc9v-=-9h5rHeh?ZTB?uAKYxDxv8zRgJy?uP-Kn?57kT?3Kp!202RROdY!a1XRy3UVc5S/UPzG4zCsUbT-Pr3nnuW0fhCTp93L"
                            response_village = requests.get(url)
                            block_data = json.loads(response_village.text)
                            
                            if block_data[0]['is_error'] == '0':
                                for block_item in block_data[1:]:
                                    block_name = block_item['BlockName']


                                    district = District.objects.filter(name=district_name).first()

                                    if district:
                                        url = "http://127.0.0.1:8000/block_create/"
                                        payload = json.dumps({
                                            "name": block_name,
                                            "district": district.pk
                                        })
                                        headers = {
                                            'Authorization': 'token ' + token,
                                            'Content-Type': 'application/json'  
                                        }
                                        response_block = requests.post(url, headers=headers, data=payload)
                                        print(response_block.text)

            return redirect('/home')
        time.sleep(86400) #
from django.shortcuts import render
from .models import Programs

# def programs_view(request):
#     Program = Programs.objects.all()
#     context = {
#         'program': program
#     }
#     return render(request, 'Student_template/programs.html', context)
def programslist_view(request):

    Program = Programs.objects.all()

    context={
        "Program" :program
    }

    return render(request, "Student_template/programs.html",context)

from django.shortcuts import render
from .models import Mentor

def all_mentors(request):
    mentors = Mentor.objects.all()
    context = {
        'mentors': mentors,
    }
    return render(request, 'Student_template/mentors.html', context)

from django.shortcuts import render
from .models import State,Block

def all_states(request):
    states = State.objects.all()
    context = {'states': states}
    return render(request, 'Student_template/states.html', context)

def all_blocks(request):
    blocks = Block.objects.all()
    context = {'blocks': blocks}
    return render(request, 'Student_template/blocks.html', context)

from django.shortcuts import render

from .models import State_allocation,Block_allocation

def state_alloc(request):
    state_allocs = State_allocation.objects.all()
    context = {
        'state_allocs': state_allocs
    }
    return render(request, 'Student_template/state_alloc.html', context)

def show_allocated_blocks(request):
    allocated_blocks = Block_allocation.objects.all()
    return render(request, 'student_template/block_alloc.html', {'allocated_blocks': allocated_blocks})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Programs, State, ProgramAllocation
from datetime import datetime

def program_state_form(request):
    programs = Programs.objects.all()
    states = State.objects.all()
    allocations = ProgramAllocation.objects.all()

    if request.method == 'POST':
        program_id = request.POST.get('program')
        state_id = request.POST.get('state')

        # Check if program allocation already exists
        allocation_exists = ProgramAllocation.objects.filter(program_id=program_id, state_id=state_id).exists()

        if allocation_exists:
            messages.error(request, 'Program allocation already exists.')
        else:
            program = Programs.objects.get(id=program_id)
            program_allocation = ProgramAllocation(program=program, state_id=state_id, allocation_date=datetime.now())
            program_allocation.allocation_time = datetime.now().time()

            program_allocation.save()
            messages.success(request, 'Program allocation created successfully.')

        return redirect('programalloc')

    context = {
        'programs': programs,
        'states': states,
        'allocations': allocations
    }
    return render(request, 'student_template/program_alloc.html', context)



# def program_state_form(request):
#     states = State.objects.filter(status=True)
#     programs = Programs.objects.all()
#     if request.method == 'POST':
#         selected_program = request.POST.get('program')
#         selected_state = request.POST.get('state')
#     return render(request, 'student_template/program_alloc.html', {'states': states, 'programs': programs})
