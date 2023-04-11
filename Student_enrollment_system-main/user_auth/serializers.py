from rest_framework import serializers
from .models import CustomUser,UserAdmin,Stateuser,Blockuser,Students,Programs,State_allocation,Block_allocation,State,Block,Work_Allocation,Bulk_File

# Serializer for the UserType model
class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

#
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username','email','password','id','first_name','phone_number']
    
    def create(self, validated_data):
            """ This creates an Admin User instance """

            new_admin = CustomUser(
                username=validated_data['username'],
                email=validated_data['email']            
            )

            new_admin.set_password(validated_data['password'])
            new_admin.save()

            return new_admin

# class PlainTextCharField(serializers.CharField):
#     def to_representation(self, value):
#         return value
class UsersSerializer(serializers.ModelSerializer):
    # password = PlainTextCharField()
    class Meta:
        model = CustomUser
        fields = ['username','email','password','id','first_name','phone_number']
    
    def update(self, instance, validated_data):
            """ This updates the user password """
            password = validated_data.pop('password', None)
            if password:
                instance.set_password(password)
            return super().update(instance, validated_data)
    
    def soft_delete(self):
        self.deleted = True
        self.save()
    
class created_bySerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username']




class UserStateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_by=created_bySerializer(read_only=True)
    username = serializers.CharField(write_only=True,required=True)
    email = serializers.EmailField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = Stateuser
        fields = '__all__'

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    # def validate_username(self)
    # or clean data

# #create state by admin
# class State_create(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)
#     class Meta:
#         model = State
#         fields = '__all__'
#     def validate_name(self, value):
#         if State.objects.filter(name=value).exists():
#             raise serializers.ValidationError("This state already created")
#         return value





# block user serializer
class BlockUserSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True,required=True)
    email = serializers.EmailField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = Blockuser
        fields = '__all__'

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

# #create block/district
# class BlockcreateSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)
#     # state=State_create(read_only=True)
#     class Meta:
#         model = district
#         fields = '__all__'






# #block allocate serializers
# class BlockallocateSerializer(serializers.ModelSerializer):
#     village=VillageSerializer(read_only=True, many=True)
#     # user = BlockUserSerializer(read_only=True)
#     # state_allocated=StateallocateSerializer(many=True)
#     created_by=UserSerializer(read_only=True)
#     class Meta:
#         model = Block_allocation
#         fields = '__all__'
#         # print(fields)

#     def validate_block_allocated(self, value):
#         if Block_allocation.objects.filter(block_allocated=value).exists():
#             raise serializers.ValidationError("Block already asigned to different user")
#         return value

class AdminUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True,required=True)
    email = serializers.EmailField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)
    first_name=serializers.CharField(write_only=True,required=True)
    phone_number=serializers.IntegerField(write_only=True,required=True)

    def validate(self, data):
        if not data.get('username'):
            raise serializers.ValidationError("Username is required")
        if not data.get('email'):
            raise serializers.ValidationError("Email is required")
        if not data.get('password'):
            raise serializers.ValidationError("Password is required")
        if not data.get('first_name'):
            raise serializers.ValidationError("First name is required")
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required")
        return data

    class Meta:
        model = UserAdmin
        fields = '__all__'




# class ProgramSerializer(serializers.ModelSerializer):
#     student=StudentSerializer(many=True,read_only=True)
#     created_by = UserSerializer(read_only=True)
#     class Meta:
#         model = Programs
#         fields = '__all__'

    def validate_program_name(self, value):
        if Programs.objects.filter(program_name=value).exists():
            raise serializers.ValidationError("Program_name already exists.")
        return value

class ProgramSerializer(serializers.ModelSerializer):
    # student=StudentSerializer(many=True,read_only=True)
    created_by = created_bySerializer(read_only=True)
    class Meta:
        model = Programs
        fields = '__all__'

    def validate_program_name(self, value):
        if Programs.objects.filter(program_name=value).exists():
            raise serializers.ValidationError("This Program already created")
        return value


from .models import S_Group, Group_Student
#create_group
class GroupSerializer(serializers.ModelSerializer):
    created_by=created_bySerializer(read_only=True)
    class Meta:
        model= S_Group
        fields ='__all__'

class StudentexcelSerializer(serializers.ModelSerializer):
    mentor_name = serializers.CharField(source='mentor.name')

    class Meta:
        model = Students
        fields = ['id', 'program', 'email', 'phone', 'address', 'mentor_name']



class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)


    # program_id = ProgramSerializer(read_only=False)

    # group_id = GroupSerializer(read_only=True)
    # village_id = VillageSerializer(read_only=True)
    # enrollment_id=serializers.CharField(max_length=250)
    # gender=serializers.CharField(write_only=True,required=True)
    created_by=created_bySerializer(read_only=True)
    # phone_number=serializers.IntegerField(write_only=True,required=True)
    class Meta:
        model = Students
        fields = '__all__'

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
#         return value
    
from .models import Mentor
class MentorSerializer(serializers.ModelSerializer):
    
    created_by = created_bySerializer(read_only=True)
  
    class Meta:
        model = Mentor
        fields = '__all__'

    # def validate_name(self, value):
    #     if village.objects.filter(name=value).exists():
    #         raise serializers.ValidationError("village already exists.")
    #     return value






class BulkFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bulk_File
        fields = ['file']


#####################################################################################################################################################################




class StudentgroupSerializer(serializers.ModelSerializer):
    # group_id=GroupSerializer(read_only=True)
    student_id=StudentSerializer(read_only=True)
    group_id=GroupSerializer(read_only=True)
    class Meta:
        model= Group_Student
        fields =['student_id','group_id']

    def validate_student(self, value):
        if Group_Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("student already exists.")
        return value


#########################################################################################################################################################
#work allocation

class Work_Allocation_serializer(serializers.ModelSerializer):
    created_by=created_bySerializer(read_only=True)
    #commeneted this giving error while creating the work allocation
    # student_id=StudentSerializer(read_only=True)
    class Meta:
        model=Work_Allocation
        fields = '__all__'

class StudentsSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    mentor_name=MentorSerializer(read_only=False)


    program_id = ProgramSerializer(read_only=False)

    group_id = GroupSerializer(read_only=True)
    # village_id = VillageSerializer(read_only=True)
    # enrollment_id=serializers.CharField(max_length=250)
    # gender=serializers.CharField(write_only=True,required=True)
    created_by=created_bySerializer(read_only=True)
    # phone_number=serializers.IntegerField(write_only=True,required=True)
    class Meta:
        model = Students
        fields = '__all__'

###################################################################################################
#get state student serializer to state user
from .models import village

class VillagedataSerializer(serializers.ModelSerializer):
    created_by = created_bySerializer(read_only=True)
    students=StudentsSerializer(many=True,read_only=True)
    block = serializers.StringRelatedField(source='block.name', read_only=True)
    state = serializers.StringRelatedField(source='block.district.state.name', read_only=True)
    district = serializers.StringRelatedField(source='block.district.name', read_only=True)

    # state=State_create(read_only=True)
    class Meta:
        model = village
        fields = '__all__'

        
class InactiveVillagedataSerializer(serializers.ModelSerializer):
    created_by = created_bySerializer(read_only=True)
    block = serializers.StringRelatedField(source='block.name', read_only=True)
    state = serializers.StringRelatedField(source='block.district.state.name', read_only=True)
    district = serializers.StringRelatedField(source='block.district.name', read_only=True)

    class Meta:
        model = village
        fields = '__all__'


class VillageSerializer(serializers.ModelSerializer):
    created_by = created_bySerializer(read_only=True)
    students=StudentsSerializer(many=True,read_only=True)
    # block = serializers.StringRelatedField(source='block.name', read_only=True)
    # state = serializers.StringRelatedField(source='block.state.name', read_only=True)

    # state=State_create(read_only=True)
    class Meta:
        model = village
        fields = '__all__'

    def validate_name(self, value):
        block = self.context['request'].data.get('block', None)  # get the block from the request data
        if block:
            # check if the village already exists in the same block
            if village.objects.filter(name=value, block=block).exists():
                raise serializers.ValidationError("A village with this name already exists in this block.")
        else:
            # if block is not provided in the request data, check if the village already exists in any block
            if village.objects.filter(name=value).exists():
                raise serializers.ValidationError("A village with this name already exists.")
        return value



  
        
        

    # def validate_name(self, value):
    #     print("*************** the value",value)
    #     block_id=village.objects.filter(block_id=)
    #     if village.objects.filter(name=value).exists():
    #         raise serializers.ValidationError("village already exists.")
    #     return value

class State_students_serializer(serializers.Serializer):
    village = VillageSerializer(many=True,read_only=True)
    class Meta:
        model=Block
        fields = '__all__'

# from .models import District
# class DistrictcreateSerializer(serializers.ModelSerializer):
#     # village = VillageSerializer(many=True,read_only=True)
#     created_by = created_bySerializer(read_only=True)
#     # state=State_create(read_only=True)
#     class Meta:
#         model = District
#         fields = '__all__'

#     def validate_name(self, value):
#         if District.objects.filter(name=value).exists():
#             raise serializers.ValidationError("District already exists.")
#         return value



#create block/district
class BlockcreatesSerializer(serializers.ModelSerializer):
    # village = VillageSerializer(many=True,read_only=True)
    # created_by = created_bySerializer(read_only=True)
    # state=State_create(read_only=True)
    class Meta:
        model = Block
        fields = '__all__'



class BlockcreateSerializer(serializers.ModelSerializer):
    village = VillageSerializer(many=True,read_only=True)
    created_by = created_bySerializer(read_only=True)
    # state=State_create(read_only=True)
    class Meta:
        model = Block
        fields = '__all__'

    # def validate_name(self, value):
    #     if Block.objects.filter(name=value).exists():
    #         raise serializers.ValidationError("Block already exists.")
    #     return value
    
    # def validate_name(self, value):
    #     district = self.context['request'].data.get('district', None)  # get the block from the request data
    #     if district:
    #         # check if the village already exists in the same block
    #         if Block.objects.filter(name=value, district=district).exists():
    #             raise serializers.ValidationError("A block with this name already exists in this block.")
    #     else:
    #         # if block is not provided in the request data, check if the village already exists in any block
    #         if Block.objects.filter(name=value).exists():
    #             raise serializers.ValidationError("A block with this name already exists.")
    #     return value
    

    def validate_name(self, value):
        district = self.context['request'].data.get('district', None)
        if district:
            # check if the block already exists in the same district
            if Block.objects.filter(name=value, district=district).exists():
                raise serializers.ValidationError("A block with this name already exists in this district.")
        else:
            # check if the block already exists in any district
            if Block.objects.filter(name=value).exists():
                raise serializers.ValidationError("A block with this name already exists.")
        return value



class BlockvalidatorSerializer(serializers.ModelSerializer):
    # village = VillageSerializer(many=True,read_only=True)
    created_by = created_bySerializer(read_only=True)
    # state=State_create(read_only=True)
    class Meta:
        model = Block
        fields = '__all__'

#block allocate serializers need to wprk imp
class BlockallocateSerializer(serializers.ModelSerializer):
    block=BlockcreateSerializer(read_only=True,many=True)
    # dist = State_students_serializer(read_only=True, many=True)
    # village=VillageSerializer(read_only=True, many=True)
    # students=StudentSerializer(many=True,read_only=True)
# if no need of full data of user then comment it
    # user = UserSerializer(read_only=True)
    # state_allocated=StateallocateSerializer(many=True)
    created_by=created_bySerializer(read_only=True)
    class Meta:
        model = Block_allocation
        fields = '__all__'
        # print(fields)

    # def validate_block_allocated(self, value):
    #     if Block_allocation.objects.filter(block_allocated=value).exists():
    #         raise serializers.ValidationError("Block already asigned to different user")
    #     return value


class BlockallocatesSerializer(serializers.ModelSerializer):
    # block=BlockcreateSerializer(read_only=True,many=True)
    # dist = State_students_serializer(read_only=True, many=True)
    # village=VillageSerializer(read_only=True, many=True)
    # students=StudentSerializer(many=True,read_only=True)
# if no need of full data of user then comment it
    # user = UserSerializer(read_only=True)
    # state_allocated=StateallocateSerializer(many=True)
    created_by=created_bySerializer(read_only=True)
    class Meta:
        model = Block_allocation
        fields = '__all__'
        # print(fields)

    def validate_block_allocated(self, value):
        if Block_allocation.objects.filter(block_allocated=value).exists():
            raise serializers.ValidationError("Block already asigned to different user")
        return value

# this is for only get allocated block and user and village and student included 
class B_allocateSerializer(serializers.ModelSerializer):
    block=BlockcreateSerializer(read_only=True)
# if no need of full data of user then comment it
    user = UserSerializer(read_only=True)
    created_by=created_bySerializer(read_only=True)
    class Meta:
        model = Block_allocation
        fields = '__all__'


#create state by admin
class State_createseri(serializers.ModelSerializer):
    # village=VillageSerializer(read_only=True, many=True)
    # students=StudentSerializer(many=True,read_only=True)

    created_by = created_bySerializer(read_only=True)
    class Meta:
        model = State
        fields = '__all__'


class State_create(serializers.ModelSerializer):
    village=VillageSerializer(read_only=True, many=True)
    students=StudentSerializer(many=True,read_only=True)
    district= State_students_serializer(many=True,read_only=True)

    created_by = created_bySerializer(read_only=True)
    class Meta:
        model = State
        fields = '__all__'
    def validate_name(self, value):
        if State.objects.filter(name=value).exists():
            raise serializers.ValidationError("This state already created")
        return value
    

from .models import District
class DistrictSerializer(serializers.ModelSerializer):
    created_by = created_bySerializer(read_only=True)
    class Meta:
        model = District
        fields = '__all__'
    def validate_name(self, value):
        if District.objects.filter(name=value).exists():
            raise serializers.ValidationError("This state already created")
        return value
    
    
class ProgramSerializer(serializers.ModelSerializer):
    # student=StudentSerializer(many=True,read_only=True)
    created_by = created_bySerializer(read_only=True)
    # state = serializers.StringRelatedField(source='programs.state.name', read_only=True)
    
    class Meta:
        model = Programs
        fields = '__all__'

    def validate_program_name(self, value):
        if Programs.objects.filter(program_name=value).exists():
            raise serializers.ValidationError("This Program already created")
        return value
    


#all deatails get serializers
#state allocate serializers
class StateallocateSerializer(serializers.ModelSerializer):
    # allocation = serializers.BooleanField(default=False)
    # state_user = UserSerializer(read_only=True)
    # state_name=State_create(read_only=True)
    allocated_by=created_bySerializer(read_only=True)
    class Meta:
        model = State_allocation
        fields = '__all__'

    def validate_state_allocated(self, value):
        if State_allocation.objects.filter(state_allocated=value).exists():
            raise serializers.ValidationError("State already asigned to different user")
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        user.allocation = True
        user.save()
        return user



#state allocate serializers
class StateallocategetSerializer(serializers.ModelSerializer):
    # allocation = serializers.BooleanField(default=False)
    state_user = UserSerializer(read_only=True)
    state_name=State_create(read_only=True)

    allocated_by=created_bySerializer(read_only=True)
    class Meta:
        model = State_allocation
        fields = '__all__'



class BlockallocategetSerializer(serializers.ModelSerializer):
    # allocation = serializers.BooleanField(default=False)
    user = UserSerializer(read_only=True)
    block=BlockcreateSerializer(read_only=True)

    allocated_by=created_bySerializer(read_only=True)
    class Meta:
        model = Block_allocation
        fields = '__all__'






from .models import Mentor
class MentorsSerializer(serializers.ModelSerializer):
    # state= State_create(read_only=True)
    # block= BlockcreateSerializer(read_only=True)
    # village= VillageSerializer(read_only=True)
    # created_by = created_bySerializer(read_only=True)
  
    class Meta:
        model = Mentor
        fields = '__all__'

class Work_Allocation_getserializer(serializers.ModelSerializer):
    created_by=created_bySerializer(read_only=True)
    student_id=StudentSerializer(read_only=True)
    class Meta:
        model=Work_Allocation
        fields = '__all__'



class VillagesSerializer(serializers.ModelSerializer):
    created_by = created_bySerializer(read_only=True)
    # students=StudentsSerializer(many=True,read_only=True)
    # state=State_create(read_only=True)
    class Meta:
        model = village
        fields = '__all__'


class StudentssSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    mentor_name=MentorSerializer(read_only=False)


    program_id = ProgramSerializer(read_only=False)

    group_id = GroupSerializer(read_only=True)
    village_id = VillagesSerializer(read_only=True)
    # enrollment_id=serializers.CharField(max_length=250)
    # gender=serializers.CharField(write_only=True,required=True)
    created_by=created_bySerializer(read_only=True)
    # phone_number=serializers.IntegerField(write_only=True,required=True)
    class Meta:
        model = Students
        fields = '__all__'


class StateallocatesSerializer(serializers.ModelSerializer):
    # allocation = serializers.BooleanField(default=False)
    # state_user = UserSerializer(read_only=True)
    state_name=State_create(read_only=True)
    allocated_by=created_bySerializer(read_only=True)
    class Meta:
        model = State_allocation
        fields = '__all__'


class StudentSSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    mentor_name=MentorSerializer(read_only=False)


    program_id = ProgramSerializer(read_only=False)

    group_id = GroupSerializer(read_only=True)
    village_id = VillagesSerializer(read_only=True)
    state= State_createseri(read_only=True)
    block= BlockcreatesSerializer(read_only=True)

    created_by=created_bySerializer(read_only=True)
    # phone_number=serializers.IntegerField(write_only=True,required=True)
    class Meta:
        model = Students
        fields = '__all__'

