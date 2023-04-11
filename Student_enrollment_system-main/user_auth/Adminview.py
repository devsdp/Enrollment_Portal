from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserTypeSerializer,DistrictSerializer,UserStateSerializer,BlockUserSerializer,BlockcreateSerializer,StudentSerializer,AdminUserSerializer,StateallocateSerializer,BlockallocateSerializer,UserSerializer,State_create
from .models import CustomUser,Stateuser,UserAdmin,Blockuser,Students,State_allocation,Block_allocation,State,Block
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from django.db import IntegrityError
from django.core.exceptions import ValidationError  
from django.contrib.auth.hashers import make_password
from django.db.models import Prefetch
from rest_framework import status  


#admin dashboard
class admin_dashboard(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=UserAdmin.objects.all()
    serializer_class= AdminUserSerializer
    def get(self, request, *args, **kwargs):
      obj =self.queryset.filter(user=self.request.user)
      # user=self.request.user
    #   print(obj)
      # return State_allocation.objects.get(user=user)
      return Response (self.serializer_class(instance=obj,many=True).data)

from django.shortcuts import get_object_or_404
import datetime
class Admincreate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=UserAdmin.objects.all()
    serializer_class= AdminUserSerializer
    
    def create(self, request, *args, **kwargs):
        password = self.request.data.get('password')
        email = self.request.data.get('email')
        state = self.request.data.get('state')
        # district = self.request.data.get('district')
        block = self.request.data.get('block')
        first_name = self.request.data.get('first_name')
        phone_number = self.request.data.get('phone_number')
            
        # Get state and block objects
        state_obj = get_object_or_404(State, id=state)
        # district_obj = get_object_or_404(District, id=district)
        block_obj = None
        block_name = ""
        if block:
            block_obj = get_object_or_404(Block, id=block)
            block_name = block_obj.name
            
        # Get state abbreviation and current date
        state_abbr = state_obj.abbreviation
        date_str = datetime.datetime.now().strftime('%Y%m%d')

        if state and block:
            # Create block user
            username = f"{state_abbr}{block_name}{first_name}"
            user = CustomUser.objects.create(username=username, email=email, user_type=3, password=make_password(password), phone_number=phone_number, first_name=first_name)
            admin = UserAdmin.objects.create(user=user, state=state_obj, block=block_obj)
            allocation=Block_allocation.objects.create(user=user,block=block_obj,created_by=self.request.user)
            admin.save()
            return Response({"status": True, "results": "Block User created sucessfully"}, status=status.HTTP_201_CREATED)

        elif state and not block:
            # Create state user
            username = f"{state_abbr}{first_name}"
            user = CustomUser.objects.create(username=username, email=email, user_type=2, password=make_password(password), phone_number=phone_number, first_name=first_name)
            admin = UserAdmin.objects.create(user=user, state=state_obj)
            allocation=State_allocation.objects.create(state_user=user,state_name=state_obj,allocated_by=self.request.user)
            admin.save()
            return Response({"status": True, "results": "State User created sucessfully"}, status=status.HTTP_201_CREATED)

        else:
            # Create admin user
            username = f"admin{date_str}"
            user = CustomUser.objects.create(username=username, email=email, user_type=1, password=make_password(password), phone_number=phone_number, first_name=first_name)
            admin = UserAdmin.objects.create(user=user)
            admin.save()
            return Response({"status": True, "results": "Admin User created sucessfully"}, status=status.HTTP_201_CREATED)


class Blockusercreate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=UserAdmin.objects.all()
    serializer_class= AdminUserSerializer
    
    def create(self, request, *kwargs):
        password = self.request.data.get('password')
        email = self.request.data.get('email')
        state = self.request.data.get('state')
        district = self.request.data.get('district')
        block = self.request.data.get('block')
        first_name = self.request.data.get('first_name')
        phone_number = self.request.data.get('phone_number')
            
        # Get state and block objects
        state_obj = get_object_or_404(State, id=state)
        district_obj = get_object_or_404(District, id=district)
        print(district_obj)
        block_obj = None
        block_name = ""
        if block:
            block_obj = get_object_or_404(Block, id=block)
            block_name = block_obj.name
            
        # Get state abbreviation and current date
        state_abbr = state_obj.abbreviation
        date_str = datetime.datetime.now().strftime('%Y%m%d')

        if state and block:
            if self.request.user.user_type == 2 and self.request.user.state.id == int(state):
                # Create block user by state user
                username = f"{state_abbr}{block_name}{first_name}"
                user = CustomUser.objects.create(username=username, email=email, user_type=3, password=make_password(password), phone_number=phone_number, first_name=first_name)
                admin = UserAdmin.objects.create(user=user, state=state_obj,district=district_obj, block=block_obj)
                allocation=Block_allocation.objects.create(user=user,block=block_obj,created_by=self.request.user)
                admin.save()
                return Response({"status": True, "results": "Block User created sucessfully"}, status=status.HTTP_201_CREATED)
            else:
                # Create block user by admin
                username = f"{state_abbr}{block_name}{first_name}"
                user = CustomUser.objects.create(username=username, email=email, user_type=3, password=make_password(password), phone_number=phone_number, first_name=first_name)
                admin = UserAdmin.objects.create(user=user, state=state_obj,district=district_obj, block=block_obj)
                allocation=Block_allocation.objects.create(user=user,block=block_obj,created_by=self.request.user)
                admin.save()
                return Response({"status": True, "results": "Block User created sucessfully"}, status=status.HTTP_201_CREATED)

class AdminGet(generics.ListAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset = UserAdmin.objects.all()
    serializer_class = AdminUserSerializer
    def get(self, request, *args, **kwargs):
      obj = self.queryset.filter(user__user_type=1)
    #   print(obj)

      return Response (self.serializer_class(instance=obj,many=True).data)

from rest_framework.pagination import PageNumberPagination
from student.pegination import StandardResultsSetPagination

class All_users(generics.ListAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(deleted=False)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    #   obj = self.queryset.filter(user__user_type=1)
    #   print(obj)

    #   return Response (self.serializer_class(instance=obj,many=True).data)
from .serializers import UsersSerializer
class Update_All_users(generics.RetrieveUpdateDestroyAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UsersSerializer
    def perform_update(self, serializer):
        password = self.request.data.get('password', None)
        if password:
            serializer.instance.set_password(password)
        serializer.save()


    def perform_destroy(self, instance):
        instance.soft_delete()




#create state user by admin only
class Stateusercreate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset=Stateuser.objects.all()
    serializer_class= UserStateSerializer
    def perform_create(self, serializer):
        print('********')
        password=self.request.data.get('password')
        username=self.request.data.get('username')
        email=self.request.data.get('email')
        created_by=self.request.user.id
        print(created_by)
        try:
            user = CustomUser.objects.create(username=username,email=email,user_type=2,password=make_password(password))
            custom_id = CustomUser.objects.get(id = created_by)
            print("&&%^^$$$")
            state=Stateuser.objects.create(created_by=custom_id, user=user)
            # state = Stateuser.objects.create(created_by=self.request.user, user=user)
            # state.save()

            # serializer.save(created_by= self.request.user)
            # user.stateuser.created_by = created_by
            # user.save()
            # qury = Stateuser.objects.create(user=user,created_by=created_by)
            # print(qury)
            # serili = UserStateSerializer(qury=qury)

            # print(password)
            return (state.data)
        except IntegrityError:
            pass



class StateGet(generics.ListAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset = CustomUser.objects.filter(user_type="2")
    serializer_class = UserSerializer
    # def get(self, request, *args, **kwargs):
    #   obj = self.queryset.filter(user__user_type=2)
    # #   print(obj)

    #   return Response (self.serializer_class(instance=obj,many=True).data)

class Stateuserupdate(generics.UpdateAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=CustomUser.objects.filter(user_type=2)
    serializer_class= UserStateSerializer
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# state allocation to state user by admin only
class Stateallocateview(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    # queryset=State_allocation.objects.all()
    queryset=State_allocation.objects.all()
    serializer_class= StateallocateSerializer
    def perform_create(self, serializer):
        state_user=self.request.data.get('state_user')
        print(state_user)

        # created_by=self.user
        # UserSerializer.allocation = True
        serializer.save(allocated_by=self.request.user)
        CustomUser.objects.filter(id=state_user).update(allocation=True)

from .serializers import StateallocategetSerializer

# state allocation to state user by admin only
class Stateallocategetview(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    # queryset=State_allocation.objects.all()
    queryset=State_allocation.objects.all()
    serializer_class= StateallocategetSerializer

        
        
   
from .serializers import StateallocatesSerializer
    # staff = Staffs.objects.get(admin=staff_id)
class allocatedstateupdate(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset=State_allocation.objects.all()
    serializer_class= StateallocatesSerializer 


# state create by admin only
class StateCount(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset=State.objects.all()
    serializer_class= State_create
    def get(self, request):
        user_count = State.objects.count()
        return Response({'count': user_count})
    

from .models import District

class DistrictCount(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset=District.objects.all()
    serializer_class= DistrictSerializer
    def get(self, request):
        user_count = District.objects.count()
        return Response({'count': user_count})


# state create by admin only
class Statecreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=State.objects.all()
    serializer_class= State_create
    def perform_create(self, serializer):
        # created_by=self.user
        serializer.save(created_by=self.request.user)


# state create by admin only
class Stateupdate(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset=State.objects.all()
    serializer_class= State_create


from .models import District
# District create by admin only
class Districtcreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=District.objects.all()
    serializer_class= DistrictSerializer
    # def perform_create(self, serializer):
    #     # created_by=self.user
    #     serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(created_by=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




# state create by admin only
class Districtupdate(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset=District.objects.all()
    serializer_class= DistrictSerializer  
    

#create block user by admin only
class Blockcreate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Blockuser.objects.all()
    serializer_class= BlockUserSerializer
    def perform_create(self, serializer):
        print('@@@@@@@@@@@@@@@')
        password=self.request.data.get('password')
        username=self.request.data.get('username')
        email=self.request.data.get('email')
        user_type=self.request.data.get('user_type')
        try:
            user = CustomUser.objects.create(username=username,email=email,user_type=user_type,password=make_password(password))
            serili = UserStateSerializer(query=user)

            print(password)
            return (serili.data)
        except IntegrityError:
            pass



class BlockGet(generics.ListAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class =UserSerializer
    def get(self, request, *args, **kwargs):
      obj = self.queryset.filter(user_type=3)
    #   print(obj)

      return Response (self.serializer_class(instance=obj,many=True).data)

# state create by admin only
class BlockCount(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset=Block.objects.all()
    serializer_class= BlockcreateSerializer
    def get(self, request):
        user_count = Block.objects.count()
        return Response({'count': user_count})

from .serializers import BlockallocatesSerializer
from .permissions import IsAllocatedToBlock
# block allocation to block user by admin only
class Blockallocateview(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Block_allocation.objects.all()
    serializer_class= BlockallocatesSerializer
   
        
    def perform_create(self, serializer):
        user=self.request.data.get('user')
        print(user)
        # created_by=self.user
        
        serializer.save(created_by=self.request.user)
        CustomUser.objects.filter(id=user).update(allocation=True)


# block allocation to block user by admin only
class AllocatedBlockupdateview(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Block_allocation.objects.all()
    serializer_class= BlockallocateSerializer


from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# district/block create by admin only
class Blockcreates(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Block.objects.all()
    serializer_class= BlockcreateSerializer
    def perform_create(self, serializer):
        # created_by=self.user
        serializer.save(created_by=self.request.user)
    
    @method_decorator(cache_page(60 * 60 * 2))  # cache for 2 hours
    def get(self, request, *args, **kwargs):
        cache_key = f"Blockcreates:{request.user.pk}"  # create a cache key
        queryset = cache.get(cache_key)  # try to get the data from the cache
        if queryset is None:
            queryset = super().get_queryset().filter(created_by=request.user).select_related( 'created_by','district')
            cache.set(cache_key, queryset)  # save the data to the cache
        return Response(self.serializer_class(instance=queryset, many=True).data)



# district allocation to block user by admin only
class Blockupdateview(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Block.objects.all()
    serializer_class= BlockcreateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#create Student user by Block user only
class Studentcreate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    #have to asdd permission to block user to create student
    permission_classes = [IsAuthenticated]
    queryset=Students.objects.all()
    serializer_class= StudentSerializer
    def perform_create(self, serializer):
        print('@@@@@@@@@@@@@@@')
        password=self.request.data.get('password')
        username=self.request.data.get('username')
        email=self.request.data.get('email')
        add=self.request.data.get('address')
        print(add)
        try:
            user = CustomUser.objects.create(username=username,email=email,user_type=4,password=make_password(password))
            # qury = State.objects.create(admin=user,address=add)
            # print(qury)
            # serili = UserStateSerializer(query=qury)

            print(password)
            return (user.data)
        except IntegrityError:
            pass



class StudentGet(generics.ListAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,IsAdminUser]
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    def get(self, request, *args, **kwargs):
      obj = self.queryset.filter(user__user_type=4)
    #   print(obj)

      return Response (self.serializer_class(instance=obj,many=True).data)
   

from .models import S_Group,Group_Student
from .serializers import GroupSerializer,StudentgroupSerializer
from .permissions import Is_block_user

class Groupcreate(generics.ListCreateAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,Is_block_user]
    queryset=S_Group.objects.all()
    serializer_class= GroupSerializer
    def perform_create(self, serializer):
        # created_by=self.user
        serializer.save(created_by=self.request.user)



class Groupget(generics.RetrieveUpdateDestroyAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication,Is_block_user]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=S_Group.objects.all()
    serializer_class= GroupSerializer
  

class StudentGroupcreate(generics.ListCreateAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Group_Student.objects.all()
    serializer_class= StudentgroupSerializer
    def perform_create(self, serializer):
        # created_by=self.user
        serializer.save(created_by=self.request.user)

    def get(self, request, *args, **kwargs):
      obj =Group_Student.objects.filter(created_by=self.request.user)
    #   user=self.request.user
      # return State_allocation.objects.get(state_user=user)
      return Response (self.serializer_class(instance=obj,many=True).data)


class GetGroupStudent(generics.ListAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Group_Student.objects.all()
    serializer_class= StudentgroupSerializer
    def get_queryset(self):
        group_id = self.kwargs['group']
        return Group_Student.objects.filter(group_id=group_id)


##########################################################################################
#all student count for admin only

# state create by admin only
class StudentCount(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Students.objects.all()
    serializer_class= StudentSerializer
    def get(self, request):
        user_count = Students.objects.count()
        return Response({'count': user_count})


from .serializers import StudentsSerializer
class All_Student(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Students.objects.all()
    serializer_class= StudentsSerializer
    def get(self, request, *args, **kwargs):
      
      obj = self.queryset.filter(status=True)
    #   print(obj)

      return Response (self.serializer_class(instance=obj,many=True).data)
    
############################################################################################################################################################
# mentor create
from .models import Mentor
from .serializers import MentorSerializer,MentorsSerializer

class Mentorcreate(generics.ListCreateAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Mentor.objects.all()
    serializer_class= MentorSerializer
    def perform_create(self, serializer):
        # created_by=self.user
        serializer.save(created_by=self.request.user)

class Mentorget(generics.ListAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Mentor.objects.all()
    serializer_class= MentorsSerializer

    def get(self, request):
        queryset = Mentor.objects.filter(status=True)
        serializer = MentorsSerializer(queryset, many=True)
        # mentor=Mentor.objects.get('mentor_name')
        data = serializer.data
        for item in data:

            village_name = item.pop('village')
            village_data= village.objects.get(id=village_name)
            item['village'] = village_data.name

            District_name = item.pop('district')
            block_data= District.objects.get(id=District_name)
            item['district'] = block_data.name

            block_name = item.pop('block')
            block_data= Block.objects.get(id=block_name)
            item['Block'] = block_data.name

            state_name = item.pop('state')
            state_data= State.objects.get(id=state_name)
            item['State'] = state_data.name
        return Response(data)
 



class Mentordetails(generics.RetrieveUpdateDestroyAPIView):
    # parser_classes = (JSONParser,)
    authentication_classes = [TokenAuthentication]
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset=Mentor.objects.all()
    serializer_class= MentorSerializer


from .serializers import VillagedataSerializer,InactiveVillagedataSerializer
from .models import village

class Villagedataview(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=village.objects.all().filter(status=True)
    serializer_class= VillagedataSerializer

class UpdateVillageStatus(generics.RetrieveUpdateAPIView):
    queryset = village.objects.all()
    serializer_class = VillagedataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(village, pk=self.kwargs['pk'])
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = not instance.status
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# class UpdateVillageStatus(generics.RetrieveUpdateAPIView):
    
#     queryset=village.objects.all()
#     serializer_class = VillagedataSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):
#         village_obj = get_object_or_404(village, pk=pk)
#         village_obj.status = not village_obj.status
#         village_obj.save()
#         serializer = VillagedataSerializer(village_obj)
#         return Response(serializer.data)
 
    
class InactiveVillagedataview(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = InactiveVillagedataSerializer

    def get_queryset(self):
        return village.objects.filter(status=False)


