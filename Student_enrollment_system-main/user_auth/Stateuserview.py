from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserTypeSerializer,UserStateSerializer,B_allocateSerializer,BlockUserSerializer,StudentSerializer,Work_Allocation_serializer,AdminUserSerializer,ProgramSerializer,StateallocateSerializer
from .models import CustomUser,Stateuser,UserAdmin,Blockuser,Students,Programs,State_allocation,Work_Allocation,State
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password

# state user dashboard
class Getallocatedstate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=State_allocation.objects.all()
    serializer_class= StateallocateSerializer
    def get(self, request, *args, **kwargs):
      obj =self.queryset.filter(state_user=self.request.user)
      # user=self.request.user
    #   print(obj)
      # return State_allocation.objects.get(state_user=user)
      return Response (self.serializer_class(instance=obj,many=True).data)


#- State level users should be able to view / download end user data with enrollment id for further uses or to manage work allocations during program planning.
from .serializers import State_students_serializer
from .models import village,Block,Block_allocation

class StudentListView(generics.ListAPIView):
  permission_classes=[IsAuthenticated]
  queryset=Block.objects.all()
  # print(queryset) 
  serializer_class = State_students_serializer
  # def get(self, request, *args, **kwargs):
  #     obj =self.queryset.filter(state_user=self.request.user)
  #     # user=self.request.user
  #     print(obj)
  #     # return State_allocation.objects.get(state_user=user)
  #     return Response (self.serializer_class(instance=obj,many=True).data)

  # def get_queryset(self):
  #     state = State_allocation.objects.get(state_user=self.request.user)
  #     print(state)
  #     # vill_id=
  #     return Students.objects.filter(village_id=state)

from rest_framework import permissions
from .serializers import BlockcreateSerializer
from .models import Block

class IsstateAllocatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        state_allocations = State_allocation.objects.filter(state_user=user)
        # print(state_allocations)
        state_ids = [state_allocation.state_name.id for state_allocation in state_allocations]
        # print (state_ids)
        # data_state_id = view.kwargs['state_id']
        return state_ids

class DataModelList(generics.ListAPIView):
    serializer_class = BlockcreateSerializer
    permission_classes = [permissions.IsAuthenticated,IsstateAllocatedUser]

    def get_queryset(self):
        user = self.request.user
        state_allocations = State_allocation.objects.filter(state_user=user)
        # print(state_allocations)
        state_ids = [state_allocation.state_name.id for state_allocation in state_allocations]
        # print (state_ids)
        # queryset=Students.objects.filter(village_id__block__state_id__in=state_ids)
        # # queryset = Block.objects.filter(state_id__in=state_ids)
        # return queryset
        queryset = Block.objects.filter(district__state_id__in=state_ids)
        return queryset
    
# get allocated block and 
class B_allocateview(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    # queryset=Block_allocation.objects.all()
    serializer_class= B_allocateSerializer
    def get_queryset(self):
        user = self.request.user
        state_allocations = State_allocation.objects.filter(state_user=user)
        # print(state_allocations)
        state_ids = [state_allocation.state_name.id for state_allocation in state_allocations]
        queryset=Block_allocation.objects.filter(block__district__state_id__in=state_ids)
        return queryset
        
from .serializers import BlockallocategetSerializer


class BlockAllocation(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Block_allocation.objects.all()
    serializer_class= BlockallocategetSerializer

from .serializers import Work_Allocation_getserializer

# work allocation by state user 
class Work_Allocate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Work_Allocation.objects.all()
    serializer_class= Work_Allocation_serializer

    def get(self, request, *args, **kwargs):
      obj =self.queryset.filter(created_by=self.request.user)
      return Response (self.serializer_class(instance=obj,many=True).data)

    def perform_create(self, serializer):
        # created_by=self.user
        serializer.save(created_by=self.request.user)


class Work_Allocate_get(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Work_Allocation.objects.all()
    serializer_class= Work_Allocation_getserializer

    def get(self, request, *args, **kwargs):
      obj =self.queryset.filter(created_by=self.request.user)
      return Response (self.serializer_class(instance=obj,many=True).data)



class Work_Allocate_update(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Work_Allocation.objects.all()
    serializer_class= Work_Allocation_serializer


from .serializers import StudentsSerializer,StudentssSerializer
from rest_framework.generics import ListAPIView

class StudentListViews(ListAPIView):
    serializer_class = StudentssSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id'] # assuming you're passing in the state id as a URL parameter
        return Students.objects.filter(village_id__block__district__state_id=state_id, status=True)
    


from rest_framework.generics import ListAPIView

class BlockStudentListViews(ListAPIView):
    serializer_class = StudentssSerializer

    def get_queryset(self):
        block_id = self.kwargs['block_id'] # assuming you're passing in the state id as a URL parameter
        return Students.objects.filter(village_id__block_id=block_id, status=True)
    

class ProgramStudentListViews(ListAPIView):
    serializer_class = StudentssSerializer

    def get_queryset(self):
        block_id = self.kwargs['program_id'] # assuming you're passing in the state id as a URL parameter
        return Students.objects.filter(program_id=block_id, status=True)




from .serializers import VillagesSerializer
from .models import village
class BlockVillagesAPIView(generics.ListAPIView):
    serializer_class = VillagesSerializer

    def get_queryset(self):
        block = self.kwargs['district_id']
        return village.objects.filter(block=block)
    


class DistrictBlockAPIView(generics.ListAPIView):
    serializer_class = BlockcreateSerializer

    def get_queryset(self):
        block = self.kwargs['district_id']
        return Block.objects.filter(district=block)
    

class VillageStudentsAPIView(generics.ListAPIView):
    serializer_class = StudentssSerializer

    def get_queryset(self):
        village_id = self.kwargs['village_id']
        return Students.objects.filter(village_id=village_id, status=True)
    
from .serializers import BlockvalidatorSerializer
from .models import Block,District

class StateBlockAPIView(generics.ListAPIView):
    serializer_class = BlockvalidatorSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id']
        district_queryset = District.objects.filter(state=state_id)
        return Block.objects.filter(district__in=district_queryset)
    


from .serializers import DistrictSerializer
class StateDistrictAPIView(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id']
        return District.objects.filter(state=state_id)
        # return Block.objects.filter(district__in=district_queryset)




from .models import Mentor, S_Group
from .serializers import   StudentexcelSerializer  


class Get_Student_with_program(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StudentexcelSerializer

    def get_queryset(self):
        # Get the user's state
        user_state = self.request.user
        print(user_state)
        
        # Filter students by their allocated program and state
        queryset = Students.objects.filter(
            program_id__state__state=user_state,
            program_id__program_name=self.kwargs['program_name'],
            status=True
        )
        
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        
        # Add additional fields to the serializer data
        data = serializer.data
        for item in data:
            mentor_id = item.pop('mentor_name')
            mentor = Mentor.objects.get(id=mentor_id)
            item['mentor_name'] = mentor.name

            program_name = item.pop('program_id')
            program = Programs.objects.get(id=program_name)
            item['program'] = program.program_name

            group_name = item.pop('group_id')
            group = S_Group.objects.get(id=group_name)
            item['group'] = group.group_name

            village_name = item.pop('village_id')
            village_data = village.objects.get(id=village_name)
            item['village'] = village_data.name

            block_name = item.pop('block')
            block_data = Block.objects.get(id=block_name)
            item['Block'] = block_data.name

            state_name = item.pop('state')
            state_data = State.objects.get(id=state_name)
            item['State'] = state_data.name
            
        return Response(data)
    

class Get_Student_with_program(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StudentexcelSerializer
    def get(self, request):
        program_id = self.request.query_params.get('program_id')
        queryset = Students.objects.filter(program_id=program_id, status=True)
        serializer = StudentSerializer(queryset, many=True)
        data = serializer.data
        for item in data:
            mentor_id = item.pop('mentor_name')
            mentor = Mentor.objects.get(id=mentor_id)
            item['mentor_name'] = mentor.name

            program_name = item.pop('program_id')
            program= Programs.objects.get(id=program_name)
            item['program'] = program.program_name

            Group_name = item.pop('group_id')
            group= S_Group.objects.get(id=Group_name)
            item['group'] = group.group_name

            state_name = item.pop('state')
            state_data= State.objects.get(id=state_name)
            item['State'] = state_data.name

            district_name = item.pop('district')
            district_data= District.objects.get(id=district_name)
            item['District'] = district_data.name

            block_name = item.pop('block')
            block_data= Block.objects.get(id=block_name)
            item['Block'] = block_data.name

            village_name = item.pop('village_id')
            village_data= village.objects.get(id=village_name)
            item['village'] = village_data.name
        return Response(data)
    
from django.shortcuts import get_object_or_404
import datetime
from rest_framework import status 
class Blockusercreatebystate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=UserAdmin.objects.all()
    serializer_class= AdminUserSerializer
    
    def create(self, request, *kwargs):
        password = self.request.data.get('password')
        email = self.request.data.get('email')
        # state = self.request.data.get('state')
        district = self.request.data.get('district')
        block = self.request.data.get('block')
        first_name = self.request.data.get('first_name')
        phone_number = self.request.data.get('phone_number')
            
        # Get state and block objects
        # state_obj = get_object_or_404(State, id=state)
        district_obj = get_object_or_404(District, id=district)
        print(district_obj)
        block_obj = None
        block_name = ""
        if block:
            block_obj = get_object_or_404(Block, id=block)
            block_name = block_obj.name
            
        # Get state abbreviation and current date
        # state_abbr = state_obj.abbreviation
        date_str = datetime.datetime.now().strftime('%Y%m%d')

        if self.request.user.user_type == 2 and not state:
            state = self.request.user._state.id
            print(state)
            
            state_obj = get_object_or_404(State, id=state)
            state_abbr = state_obj.abbreviation

            
            # Create block user by state user
            username = f"{state_abbr}{block_name}{date_str}"
            user = CustomUser.objects.create(username=username, email=email, user_type=3, password=make_password(password), phone_number=phone_number, first_name=first_name)
            admin = UserAdmin.objects.create(user=user, state=state_obj,district=district_obj, block=block_obj)
            allocation=Block_allocation.objects.create(user=user,block=block_obj,created_by=self.request.user)
            admin.save()
            return Response({"status": True, "results": "Block User created sucessfully"}, status=status.HTTP_201_CREATED)

        




    

