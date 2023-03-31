from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserTypeSerializer,UserStateSerializer,BlockUserSerializer,StudentSerializer,GroupSerializer,AdminUserSerializer,ProgramSerializer,BlockallocateSerializer
from .models import CustomUser,Stateuser,UserAdmin,Blockuser,Students,Programs,Block_allocation,S_Group
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import permissions
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from .permissions import Is_block_user,IsAdminUser,IsAllocatedToBlock
import datetime


class Getallocatedblock(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,Is_block_user,IsAllocatedToBlock]
    queryset=Block_allocation.objects.all()
    serializer_class= BlockallocateSerializer
    def get(self, request, *args, **kwargs):
      obj =Block_allocation.objects.filter(user=self.request.user)
    #   user=self.request.user
      # return State_allocation.objects.get(state_user=user)
      return Response (self.serializer_class(instance=obj,many=True).data)

###########################################################################################################################################################

from rest_framework import permissions
from .serializers import VillageSerializer
from .models import village

class IsblockAllocatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        Block_allocations = Block_allocation.objects.filter(user=user)
        print(Block_allocations)
        block_ids = [block_allocation.block.id for block_allocation in Block_allocations]
        print (block_ids)
        # data_state_id = view.kwargs['state_id']
        return block_ids

class Block_allocated_data(generics.ListAPIView):
    serializer_class = VillageSerializer
    permission_classes = [permissions.IsAuthenticated,IsblockAllocatedUser]

    def get_queryset(self):
        user = self.request.user
        Block_allocations = Block_allocation.objects.filter(user=user)
        # print(state_allocations)
        block_ids = [block_allocation.block.id for block_allocation in Block_allocations]
        # print (state_ids)
        queryset = village.objects.filter(block_id__in=block_ids)
        return queryset
    
from .serializers import StudentSSerializer
class Block_allocated_datas(generics.ListAPIView):
    serializer_class = StudentSSerializer
    permission_classes = [permissions.IsAuthenticated,IsblockAllocatedUser]

    def get_queryset(self):
        user = self.request.user
        Block_allocations = Block_allocation.objects.filter(user=user)
        # print(state_allocations)
        block_ids = [block_allocation.block.id for block_allocation in Block_allocations]
        # print (state_ids)
        queryset = Students.objects.filter(block__in=block_ids,status=True)
        return queryset








##############################################################################################################################################################
# class CreateProgram(generics.ListCreateAPIView):
#     authentication_classes = [TokenAuthentication]
#     # pagination_class = StandardResultsSetPagination
#     permission_classes = [IsAuthenticated]
#     queryset=Programs.objects.all()
#     serializer_class= ProgramSerializer
#     def perform_create(self, serializer):
#         # created_by=self.user
#         serializer.save(created_by=self.request.user)



from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class CreateProgram(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer

    def get_queryset(self):
        state = self.request.query_params.get('state', None)
        if state is not None:
            queryset = Programs.objects.filter(state=state)
        else:
            queryset = Programs.objects.all()
            # state=State.objects.filter(id=queryset)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GetstateProgram(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer

    def get_queryset(self):
        # Get the user's allocated state
        user_state = self.request.user.state_allocation.state_name.id
        
        # Filter programs by allocated state
        queryset = Programs.objects.filter(state=user_state)
        
        return queryset
    
class GetstateProgramforclockuser(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer

    def get_queryset(self):
        # Get the user's allocated state
        user_state = self.request.user.block_allocation.block.district.state.id
        
        # Filter programs by allocated state
        queryset = Programs.objects.filter(state=user_state)
        
        return queryset



class ProgramListByVillage(generics.ListAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        village_id = self.kwargs['village_id']
        village_name = village.objects.get(id=village_id)
        state = village_name.block.district.state
        queryset = Programs.objects.filter(state=state)
        return queryset


   

class Programdetailedview(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=Programs.objects.all()
    serializer_class=ProgramSerializer
    


from .models import village
from .serializers import VillageSerializer,UserSerializer
#village create by district /block user

class Villagecreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=village.objects.all()
    serializer_class= VillageSerializer
    def perform_create(self, serializer):
        # created_by=self.user
        serializer.save(created_by=self.request.user)


class Villageupdate(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=village.objects.all()
    serializer_class= VillageSerializer
    

# state create by admin only
class VillageCount(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset=village.objects.all()
    serializer_class= VillageSerializer
    def get(self, request):
        user_count = village.objects.count()
        return Response({'count': user_count})


class StudentCreateAPIView(generics.CreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


from .models import Mentor,State,Block
from rest_framework import status      
from django.core.exceptions import ValidationError  
from django.db import transaction

class Student_create(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Students.objects.all()
    serializer_class= StudentSerializer
    def get(self, request, *args, **kwargs):
      user_blocks = self.request.user.Block_allocation.all()
      print(user_blocks)
      obj =Students.objects.filter(created_by=self.request.user,block=user_blocks)
    #   user=self.request.user
      # return State_allocation.objects.get(state_user=user)
      return Response (self.serializer_class(instance=obj,many=True).data)
    
    # def perform_create(self, serializer):

    #     # created_by=self.user
    #     serializer.save(created_by=self.request.user)

    # @transaction.atomic
    def create(self, request, *args, **kwargs):
        print("%#^#^#^")
        # password=self.request.data.get('password')
        # print(password)
        enrollment=self.request.data.get('enrollment_id')
        # username=self.request.data.get('username')
        # email=self.request.data.get('email')
        gender=self.request.data.get('gender')
        print(gender)
        phone_number=self.request.data.get('phone_number')
        print(phone_number)
        mentor_name=self.request.data.get('mentor_name')
        mnt_name = Mentor.objects.get(id=mentor_name)
        print(mentor_name)
        first_name=self.request.data.get('first_name')
        last_name=self.request.data.get('last_name')
        print(last_name)
        # state=self.request.data.get('state')
        # state_name = State.objects.get(id=state)
        # print(state)
        # block=self.request.data.get('block')
        # block_name = Block.objects.get(id=block)
        village_id=self.request.data.get('village_id')
        group_id=self.request.data.get('group_id')
        program_id=self.request.data.get('program_id')
        program_data = Programs.objects.get(id=program_id)
        grp_id = S_Group.objects.get(id=group_id)
        # print(program_data)
        vill_data = village.objects.get(id=village_id)
        print(vill_data.name)
        block_id = vill_data.block
        print(block_id.name)
        district_id = vill_data.block.district
        print(district_id.name)
        state_id = vill_data.block.district.state
        print(state_id.name)
        # curent_year = datetime.now().year
        # print(curent_year)

        if program_data.state == state_id:
        # Create student
            data_std = Students.objects.create(
                group_id=grp_id,
                state=state_id,
                district=district_id,
                block=block_id,
                last_name=last_name,
                mentor_name=mnt_name,
                first_name=first_name,
                village_id=vill_data,
                program_id=program_data,
                phone_number=phone_number,
                gender=gender,
                created_by=self.request.user
            )

            new_number = data_std.id
            print("the new number is ", new_number)
            enrollment_id = f"EN{state_id.abbreviation}N{new_number:07}"
            data_std.enrollment_id = enrollment_id
            data_std.save()
            return Response({"status": True, "results": "Student created sucessfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": False, "results": "Program state and village state does not match"}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     # Get the last student record from the database and extract the last number from its enrollment ID
            
            
        #     data_std = Students.objects.create(
        #         group_id=grp_id,
        #         state=state_id,
        #         block=district_id,
        #         last_name=last_name,
        #         mentor_name=mnt_name,
        #         first_name=first_name,
        #         village_id=vill_data,
        #         program_id=program_data,
        #         phone_number=phone_number,
        #         gender=gender,
        #         created_by=self.request.user
        #     )

        #     new_number = data_std.id
        #     print("the new number is ", new_number)
        #     enrollment_id = f"EN{state_id.abbreviation}N{new_number:07}"
        #     data_std.enrollment_id = enrollment_id
        #     data_std.save()

        #     return Response({"status": True, "results": "data saved sucessfully"},status=status.HTTP_201_CREATED)
        # except ValidationError as err:
        #         return Response({"status": False, "error_description": err.detail}, status=status.HTTP_400_BAD_REQUEST)


        # with transaction.atomic():
        #     try:  
        #         data = request.data
        #         users = request.data.get('users', None)
        #         serializer = UserSerializer(data=data)
        #         if serializer.is_valid(raise_exception=True):
        #             instance = serializer.save()
        #             print(instance.id)
        #             enrollement_id = state_id.abbreviation+"_"+ district_id.name +"_"+str(curent_year)+"_"+first_name+"_"+str(instance.id)

                
        #             data_std = Students.objects.create(user=instance ,group_id=grp_id,mentor_name=mnt_name,first_name=first_name,village_id=vill_data,program_id=program_data, enrollment_id=enrollement_id,phone_number=phone_number,gender=gender,created_by=self.request.user)
        #             data_std.save()

        #             # data_user=CustomUser.objects.filter(id=instance.id).update(user_type=4,phone_number=phone_number,first_name=first_name)
                    
        #         return Response({"status": True, "results": "data saved sucessfully"},status=status.HTTP_201_CREATED)

                
        #         # serializer_std = StudentSerializer(data=data)
        #         # if serializer_std.is_valid(raise_exception=True):
        #         #     serializer_std.user = instance
        #         #     serializer_std.enrollment_id = enrollment
        #         #     serializer_std.gender = gender
        #         #     serializer_std.phone_number = phone_number
        #         #     serializer_std.save()
                
        #             # if users:
        #             #     for user in users:
        #             #         Students(user=instance.id , created_by=self.request.user)
        #             # return Response({"status": True, "results": "data saved sucessfully"},status=status.HTTP_201_CREATED)
        #     except ValidationError as err:
        #         return Response({"status": False, "error_description": err.detail}, status=status.HTTP_400_BAD_REQUEST)


# class Bulk_Student_create(generics.CreateAPIView):
#     authentication_classes = [TokenAuthentication]
#     # pagination_class = StandardResultsSetPagination
#     permission_classes = [IsAuthenticated]
#     queryset=Students.objects.all()
#     serializer_class= StudentSerializer
#     def perform_create(self, serializer):
#         students = self.request.data
#         instances = [Students(**student) for student in students]
#         Students.objects.bulk_create(instances)
import os
from datetime import datetime
from .models import Bulk_File,District 
from .serializers import BulkFileSerializer
import pandas as pd
from builtins import max
from django.http import JsonResponse

class Bulk_Student_create(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,Is_block_user]
    queryset=Bulk_File.objects.all()
    serializer_class= BulkFileSerializer
    def create(self,request):
        file = self.request.FILES['file']
        print(file)
        # base, extension = os.path.splitext(file)
        base = file.name.split(".")[0]
        # name=base
        Bulk_File.objects.create(file=file,name=base,status=False)
        if not file.name.endswith('xlsx'):
            return Response({"message":"wrong format"})
        df = pd.read_excel(file)
        print(df.columns)

        for index, row in df.iterrows():

            gender = row["gender"]
            first_name = row["first_name"]
            last_name = row["last_name"]
            print(last_name)
            # mentor_name_get = row["mentor_name"]
            


            try:
                phone_number_get = row["phone_number"]
                number=Students.objects.get(phone_number=phone_number_get)
                error_msg = 'Phone Number {} already exists'.format(phone_number_get)
                return Response({'error': error_msg}, status=400)
            except Students.DoesNotExist:
                phone_number = phone_number_get
            except KeyError:
                return Response({"message": "Phone_number column missing"}, status=status.HTTP_400_BAD_REQUEST)
                


            try:
                mentor_name_get = row["mentor_name"]
                mnt_name = Mentor.objects.get(name__iexact=mentor_name_get)
                mentor_name = Mentor.objects.get(id=mnt_name.id)
            except Mentor.DoesNotExist:
                error_msg = 'Mentor with name {} does not exist'.format(mentor_name_get)
                return Response({'error': error_msg}, status=400)
            except KeyError:
                return Response({"message": "mentor_name column missing"}, status=status.HTTP_400_BAD_REQUEST)
            


            

            try:
                state_name_get = row['state']
                state_obj = State.objects.get(name__iexact=state_name_get)
                print(state_obj)
                state_name = State.objects.get(id=state_obj.id)
                print(state_name)
            except State.DoesNotExist:
                error_msg = 'State with name {} does not exist'.format(state_name_get)
                return Response({'error': error_msg}, status=400)
            except KeyError:
                return Response({"message": "State_name column missing"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                district_get = row['district']
                district_obj = District.objects.get(name__iexact=district_get)
                print(district_obj)
                district_name = District.objects.get(id=district_obj.id)
                print(district_name)
            except District.DoesNotExist:
                error_msg = 'District with name {} does not exist'.format(district_get, state=state_obj.name)
                return Response({'error': error_msg}, status=400)
            except KeyError:
                return Response({"message": "District_name column missing"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                block_name_get=row["block"]
                block_obj = Block.objects.get(name__iexact=block_name_get, district=district_obj)
                block_name = Block.objects.get(id=block_obj.id)
            except Block.DoesNotExist:
                error_msg = 'Block with name {} does not exist in {}'.format(block_name_get, district_obj.name)
                return Response({'error': error_msg}, status=400)
            except KeyError:
                return Response({"message": "Block_name column missing"}, status=status.HTTP_400_BAD_REQUEST)
            

            try:
                village_name_get = row["village"]
                village_obj = village.objects.get(name__iexact=village_name_get, block=block_obj)
                village_name = village.objects.get(id=village_obj.id)
            except village.DoesNotExist:
                error_msg = 'Village with name {} does not exist in {}'.format(village_name_get, block_obj.name)
                return Response({'error': error_msg}, status=400)
            except KeyError:
                return Response({"message": "Village_name column missing"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                group_id=row['group_name']
                group_obj = S_Group.objects.get(group_name__iexact=group_id)
                group_id = S_Group.objects.get(id=group_obj.id)
            except S_Group.DoesNotExist:
                error_msg = 'Group with name {} does not exist'.format(group_id)
                return Response({'error': error_msg}, status=400)
            except KeyError:
                return Response({"message": "Group_name column missing"}, status=status.HTTP_400_BAD_REQUEST)
            

            try:
                program_id = row['program']
                prog_obj = Programs.objects.get(program_name__iexact=program_id)
                program_id = Programs.objects.get(id=prog_obj.id)
            except Programs.DoesNotExist:
                error_msg = 'Program with name {} does not exist'.format(program_id)
                return Response({'error': error_msg}, status=400)
            except KeyError:
                return Response({"message": "Program column missing"}, status=status.HTTP_400_BAD_REQUEST)

            
            # print(district_id.name)
            state_id = village_obj.block.district.state
            print(state_id.name)
            curent_year = datetime.now().year
            # print(curent_year)
            # if 'enrollment_id' in df.columns :
            #     enrollment_id = row['enrollment_id']
            #     # created_at= row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            #     # updated_at= row['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
            #     # date_created = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            #     # date_updated = datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')

            #     student= Students.objects.create( enrollment_id = enrollment_id,state=state_name,block=block_name,last_name=last_name,gender=gender,group_id=group_id,first_name=first_name,mentor_name=mentor_name,program_id=program_id,phone_number=phone_number,village_id=village_name,created_by=self.request.user)
            
            if 'enrollment_id' in df.columns and df['enrollment_id'].isnull().values.any():
                # if df['enrollment_id'].isnull().values.any():
                # my_col = df['enrollment_id']
                # print(my_col.isna().any())
                # elif 'enrollment_id' not in df.columns and 'created_at' in df.columns and 'updated_at' in df.columns:
                # created_at= row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                # updated_at= row['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
                # date_created = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                # date_updated = datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
                    # data_std = Students.objects.create(group_id=group_id,state=state_name,block=block_name,last_name=last_name,mentor_name=mnt_name,first_name=first_name,village_id=village_name,program_id=program_id,phone_number=phone_number,gender=gender,created_by=self.request.user)
                    # try:
                    #     # Get the last student record from the database and extract the last number from its enrollment ID
                    #     last_student = Students.objects.order_by('-id').first()
                    #     print(last_student.enrollment_id)
                    #     # last_number = Students.objects.aggregate(Max('enrollment_id'))['enrollment_id__max']
                    #     # if last_number:
                    #     #     next_number = int(last_number.split('N')[-1]) + 1
                    #     # else:
                    #     #     next_number = 1
                    #     # enrollment_id = f"EN{state_id.abbreviation}N{next_number:07}"

                    #     if last_student is not None:
                    #         last_number = int(last_student.enrollment_id.split('N')[-1])
                    #     else:
                    #         last_number = 0

                    #     # Generate the new enrollment ID by concatenating the state ID abbreviation and the next number
                    #     new_number = last_number + 1
                    #     enrollment_id = f"EN{state_id.abbreviation}N{new_number:07}"

                    
                    #     # enrollement_id = state_id.abbreviation + "_" + district_id.name + "_" + str(curent_year) + "_" + first_name + "_" + str(data_std.id)
                    #     data_std.enrollment_id = enrollement_id
                    #     data_std.save()
                    # except ValidationError as err:
                    #     return Response({"status": False, "error_description": err.detail}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    
                    data_std = Students.objects.create(group_id=group_id,state=state_name,block=block_name,district=district_name,last_name=last_name,mentor_name=mnt_name,first_name=first_name,village_id=village_name,program_id=program_id,phone_number=phone_number,gender=gender,created_by=self.request.user)
                #    Get the last student record from the database and extract the last number from its enrollment ID
                    
                    # Generate the new enrollment ID by concatenating the state ID abbreviation and the next number
                    new_number = data_std.id
                    print("the new number is ", new_number)
                    enrollment_id = f"EN{state_id.abbreviation}N{new_number:07}" 
                    
                    data_std.enrollment_id = enrollment_id
                    data_std.save()

                    # return Response({"status": True, "results": "data saved sucessfully"},status=status.HTTP_201_CREATED)
                except ValidationError as err:
                        return Response({"status": False, "error_description": err.detail}, status=status.HTTP_400_BAD_REQUEST)

            else:
                if 'enrollment_id' in df.columns :
                    enrollment_id = row['enrollment_id']
                    # created_at= row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                    # updated_at= row['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
                    # date_created = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                    # date_updated = datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')

                    student= Students.objects.create( enrollment_id = enrollment_id,state=state_name,block=block_name,district=district_name,last_name=last_name,gender=gender,group_id=group_id,first_name=first_name,mentor_name=mentor_name,program_id=program_id,phone_number=phone_number,village_id=village_name,created_by=self.request.user)
        return Response({"message": "bulk_upload_success."})
            # elif 'enrollment_id' not in df.columns and 'created_at' not in df.columns and 'updated_at' in df.columns:
            #     updated_at= row['updated_at']
            #     date_updated = datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')

            #     data_std = Students.objects.create(group_id=group_id,state=state_name,block=block_name,updated_at=date_updated,last_name=last_name,mentor_name=mnt_name,first_name=first_name,village_id=village_name,program_id=program_id,phone_number=phone_number,gender=gender,created_by=self.request.user)
            #     enrollement_id = state_id.abbreviation + "_" + district_id.name + "_" + str(curent_year) + "_" + first_name + "_" + str(data_std.id)
            #     data_std.enrollment_id = enrollement_id
            #     data_std.save()

            # elif 'enrollment_id' in df.columns and 'created_by' not in df.columns:
            #     enrollment_id = row['enrollment_id']
            #     student= Students.objects.create( enrollment_id = enrollment_id,state=state_name,block=block_name,last_name=last_name,gender=gender,group_id=group_id,first_name=first_name,mentor_name=mnt_name,program_id=prog_id,phone_number=phone_number,village_id=village_name,created_by=self.request.user)

                

                # else:
                #     student = Students.objects.create(
                #         enrollment_id=enrollment_id,
                #         state=state_name,
                #         block=block_name,
                #         last_name=last_name,
                #         gender=gender,
                #         group_id=grp_id,
                #         first_name=first_name,
                #         mentor_name=mnt_name,
                #         program_id=prog_id,
                #         phone_number=phone_number,
                #         village_id=vill_id,
                #         created_by=self.request.user
                #     )

            # else:
            #         # Generate enrollment ID if not provided in file
            #     try:
            #         data_std = Students.objects.create(group_id=group_id,state=state_name,block=block_name,last_name=last_name,mentor_name=mnt_name,first_name=first_name,village_id=village_name,program_id=prog_id,phone_number=phone_number,gender=gender,created_by=self.request.user)
            #         # enrollement_id = state_id.abbreviation+"_"+ district_id.name +"_"+str(curent_year)+"_"+first_name+"_"+self.id
            #         enrollement_id = state_id.abbreviation + "_" + district_id.name + "_" + str(curent_year) + "_" + first_name + "_" + str(data_std.id)
            #         data_std.enrollment_id = enrollement_id
            #         data_std.save()

            #         return Response({"status": True, "results": "data saved sucessfully"},status=status.HTTP_201_CREATED)
            #     except ValidationError as err:
            #             return Response({"status": False, "error_description": err.detail}, status=status.HTTP_400_BAD_REQUEST)
            
                # enrollement_id = state_id.abbreviation+"_"+ district_id.name +"_"+str(curent_year)+"_"+first_name+"_"+str(id)
                # student= Students.objects.create( enrollment_id = enrollement_id,gender=gender,group_id=grp_id,first_name=first_name,mentor_name=mentor_name,program_id=prog_id,phone_number=phone_number,village_id=vill_id,created_by=self.request.user)
        # return Response({"message": "bulk_upload_success."})
        # return render(request, 'bulk_upload_success.html')
    # return render(request, 'bulk_upload.html')
# from rest_framework import generics
# from .models import CustomUser,Students
# from .serializers import UserSerializer, StudentSerializer

# class UserBulkCreate(generics.ListCreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
                # if 'created_by' in df.columns:

#     def perform_create(self, serializer):
#         file = self.request.FILES['file']
#         df = pd.read_excel(file)
#         print(df)
#         instances = [Students(**row) for _, row in df.iterrows()]
#         CustomUser = serializer.save()

#         # Create the records in Table2
#         StudentSerializer = StudentSerializer(data={'CustomUser': CustomUser.id,})
#         if StudentSerializer.is_valid():
#             StudentSerializer.save()
#         else:
#             return Response({"message":"student serializer is not valid"})

# class StudentBulkCreate(generics.ListCreateAPIView):
#     queryset = Students.objects.all()
#     serializer_class = StudentSerializer

   


    # @transaction.atomic
    # def create(self, request, *args, **kwargs):
    #     with transaction.atomic():
    #         try:
    #             data = request.data
    #             serializer = StudentSerializer(data=data)
    #             if serializer.is_valid(raise_exception=True):
    #                 serializer.save()
    #                 # // recheck , this loop have input is all users in json
    #                 # for user in data.get('users'):
    #             user_serializer = UserSerializer(data=data)
    #             if user_serializer.is_valid(raise_exception=True):
    #               user_serializer.save()
    #               return Response({"status": True, "results": "Evento registrado correctamente"},
    #                                 status=status.HTTP_201_CREATED)
    #         except ValidationError as err:
    #             return Response({"status": False, "error_description": err.detail}, status=status.HTTP_400_BAD_REQUEST)
   
   
   
   
    # def perform_create(self,serializer):
    #     password=self.request.data.get('password')
    #     username=self.request.data.get('username')
    #     email=self.request.data.get('email')
    #     gender=self.request.data.get('gender')
    #     phone_number=self.request.data.get('phone_number')
    #     try:
    #       with transaction.atomic():
    #           user = CustomUser.objects.create(username=username,email=email,user_type=4,password=make_password(password))
    #           user=serializer.save()
    #           Students.objects.create(user=user,gender=gender,created_by=self.request.user,phone_number=phone_number)
    #     except IntegrityError:
    #         pass
    # def perform_create(self, serializer):
    #     print('@@@@@@@@@@@@@@@')
    #     password=self.request.data.get('password')
    #     username=self.request.data.get('username')
    #     email=self.request.data.get('email')
    #     enrollment_id=self.request.data.get('address')
    #     gender=self.request.data.get('gender')
    #     try:
    #         user = CustomUser.objects.create(username=username,email=email,user_type=4,password=make_password(password))
    #         print(user)
    #         user.students.gender=gender
    #         print(gender)
    #         user.save()
    #         # qury = Students.objects.create(user=user,enrollment_id=enrollment_id,gender=gender)
    #         # print(qury)
    #         # serili = StudentSerializer(query=qury)

    #         print(password)
    #         return Response(user)
    #     except IntegrityError:
    #         pass
        
    # def create(self, serializer):
    #     print('@@@@@@@@@@@@@@@')
    #     enrollment_id=self.request.data.get('address')
    #     gender=self.request.data.get('gender')
    #     try:
    #         user = Students.objects.create(gender=gender)
    #         print(user)
            
    #         print(gender)
    #         user.save()
    #         # qury = Students.objects.create(user=user,enrollment_id=enrollment_id,gender=gender)
    #         # print(qury)
    #         # serili = StudentSerializer(query=qury)
    #         return Response({"message":"created"})
    #     except IntegrityError:
    #         pass

from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .models import Mentor,village
from .serializers import StudentexcelSerializer

class Get_Student(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Students.objects.all()
    serializer_class= StudentexcelSerializer

    def get(self, request):
        queryset = Students.objects.filter(created_by=self.request.user, status=True)
        serializer = StudentSerializer(queryset, many=True)
        # mentor=Mentor.objects.get('mentor_name')
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

            village_name = item.pop('village_id')
            village_data= village.objects.get(id=village_name)
            item['village'] = village_data.name

            block_name = item.pop('block')
            block_data= Block.objects.get(id=block_name)
            item['Block'] = block_data.name

            district_name = item.pop('district')
            district_data= District.objects.get(id=district_name)
            item['District'] = district_data.name

            state_name = item.pop('state')
            state_data= State.objects.get(id=state_name)
            item['State'] = state_data.name
        return Response(data)
        # df = pd.DataFrame(data)
        # data_1 = df.drop(['file_id','id','created_by','status'], axis=1)
        # data_1.to_excel('media/my_data.xlsx', index=False)

        # return Response(data)
    

        # df = pd.DataFrame(data)
        # data_1 = df.drop(['file_id','id','created_by','status'], axis=1)

        # # Get the current date and format it as a string
        # date_str = datetime.now().strftime('%Y-%m-%d')

        # # Include the date in the filename
        # filename = f'media/my_data_{date_str}.xlsx'

        # data_1.to_excel(filename, index=False)

    # def get(self, request, *args, **kwargs):
    # #   obj =Students.objects.filter(created_by=self.request.user)
    #   students =Students.objects.filter(created_by=self.request.user)
    # #   students = self.get_queryset()

    #   buffer = BytesIO()
    #   p = canvas.Canvas(buffer)

    #   p.drawString(100, 750, "List of Students")
    #   p.drawString(100, 720, "first_name")
    #   p.drawString(250, 720, "mentor_name")

    #   y = 700
    #   for student in students:
    #         p.drawString(100, y, student.first_name)
    #         p.drawString(250, y, str(student.mentor_name))
    #         y -= 20

    #   p.showPage()
    #   p.save()

    #   buffer.seek(0)
    #   response = FileResponse(buffer, content_type='application/pdf')
    #   response['Content-Disposition'] = 'attachment; filename="students.pdf"'
    #   return response
    #   user=self.request.user
      # return State_allocation.objects.get(state_user=user)
    #   return Response (self.serializer_class(instance=obj,many=True).data)

from .permissions import LimitedTimeUpdatePermission
from .serializers import StudentsSerializer

class Student_update(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Students.objects.all()
    serializer_class= StudentSerializer
    # def get(self, request, *args, **kwargs):
    #   obj =Students.objects.filter(created_by=self.request.user)
    # #   user=self.request.user
    #   # return State_allocation.objects.get(state_user=user)
    #   return Response (self.serializer_class(instance=obj,many=True).data)

    def put(self, request, *args, **kwargs):
        # obj =Students.objects.filter(created_by=self.request.user)
    #   user=self.request.user
      # return State_allocation.objects.get(state_user=user)
        # return Response (self.serializer_class(instance=obj,many=True).data)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # gender=self.request.data.get('gender')
        # phone_number=self.request.data.get('phone_number')
        # mentor_name=self.request.data.get('mentor_name')
        # first_name=self.request.data.get('first_name')
        # village_id=self.request.data.get('village_id')
        # group_id=self.request.data.get('group_id')
        # last_name=self.request.data.get('last_name')
        # program=self.request.data.get('program_id')
        # # print("*******",int(program))
        # update_student = Students.objects.filter(id=user.id).update(program_id=int(program),gender=gender,phone_number=phone_number,mentor_name=mentor_name,first_name=first_name,village_id=village_id,group_id=group_id,last_name=last_name)
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Group_create_B(generics.ListCreateAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,Is_block_user]
    queryset=S_Group.objects.all()
    serializer_class= GroupSerializer
    def perform_create(self, serializer):
        # created_by=self.user
        serializer.save(created_by=self.request.user)

    def get(self, request, *args, **kwargs):
      obj =S_Group.objects.filter(created_by=self.request.user)
    #   user=self.request.user
      # return State_allocation.objects.get(state_user=user)
      return Response (self.serializer_class(instance=obj,many=True).data)
    


class Group_update(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=S_Group.objects.all()
    serializer_class= GroupSerializer
    # def get(self, request, *args, **kwargs):
    #   obj =Students.objects.filter(created_by=self.request.user)
    # #   user=self.request.user
    #   # return State_allocation.objects.get(state_user=user)
    #   return Response (self.serializer_class(instance=obj,many=True).data)

    def put(self, request, *args, **kwargs):
        # obj =Students.objects.filter(created_by=self.request.user)
    #   user=self.request.user
      # return State_allocation.objects.get(state_user=user)
        # return Response (self.serializer_class(instance=obj,many=True).data)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    


    


############################################################################################################

from rest_framework import generics
# from myapp.models import Student
# from myapp.serializers import StudentSerializer

class StudentList(generics.ListAPIView):
    serializer_class = StudentsSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        queryset = Students.objects.filter(group_id=group_id, status=True)
        return queryset