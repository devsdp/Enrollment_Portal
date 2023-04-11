from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "State"),(3, "Block"), (4, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    deleted = models.BooleanField(default=False)
    first_name= models.CharField(max_length=25)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    allocation=models.BooleanField(default=False)
    

    class Meta:
        db_table = "User"

    def soft_delete(self):
        self.deleted = True
        self.save()



class Stateuser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='s_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "Stateuser"


STATES = [
        ('Andhra Pradesh','Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chhattisgarh','Chhattisgarh'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Odisha','Odisha'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Telangana','Telangana'),
('Tripura','Tripura'),
('Uttar Pradesh','Uttar Pradesh'),
('Uttarakhand','Uttarakhand'),
('West Bengal','West Bengal'),
('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
('Chandigarh','Chandigarh'),
('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
('Nct Of Delhi','Nct Of Delhi'),
('Daman and Diu','Daman and Diu'),
('TestState','TestState'),
('Jammu and Kashmir','Jammu and Kashmir'),
('Lakshadweep','Lakshadweep'),
('Puducherry','Puducherry'),
    ]
#create block user model
class State(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, choices=STATES)
    abbreviation = models.CharField(max_length=3, editable=False)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='state_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    status= models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        states_abbreviations = {
           'Andhra Pradesh':'AP',
            'Arunachal Pradesh':'AR',
            'Assam':'AS',
            'Bihar':'BR',
            'Chhattisgarh':'CT',
            'Goa':'GA',
            'Gujarat':'GJ',
            'Haryana':'HR',
            'Himachal Pradesh':'HP',
            'Jharkhand':'JH',
            'Karnataka':'KA',
            'Kerala':'KL',
            'Madhya Pradesh':'MP',
            'Maharashtra':'MH',
            'Manipur':'MN',
            'Meghalaya':'ML',
            'Mizoram':'MZ',
            'Nagaland':'NL',
            'Odisha':'OR',
            'Punjab':'PB',
            'Rajasthan':'RJ',
            'Sikkim':'SK',
            'Tamil Nadu':'TN',
            'Telangana':'TG',
            'Tripura':'TR',
            'Uttar Pradesh':'UP',
            'Uttarakhand':'UT',
            'West Bengal':'WB',
            'Andaman and Nicobar Islands':'AN',
            'Chandigarh':'CH',
            'Dadra and Nagar Haveli':'DN',
            'Daman and Diu':'DD',
            'Jammu and Kashmir':'JK',
            'TestState':'TS',
            'Nct Of Delhi':'DL',
            'Lakshadweep':'LD',
            'Puducherry':'PY'
        }

        self.abbreviation = states_abbreviations.get(self.name, '')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "State"


#state_allocation 
class State_allocation(models.Model):
    id = models.AutoField(primary_key=True)
    state_user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    state_name=models.OneToOneField(State,on_delete=models.CASCADE)
    status= models.BooleanField(default=True)
    allocated_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='s_allocated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "State_allocation"

    def __str__(self):
        return str(self.state_user)



#create block user model
class Blockuser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='b_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "Blockuser"

class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE,related_name='district')
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='d_created_by')
    status= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "District"

    def __str__(self):
        return self.name



# district creation/block by admin
class Block(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE,related_name='block')
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='block_created_by')
    status= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "Block"

    def __str__(self):
        return f"{self.name} - {self.id}"



class Block_allocation(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    block=models.OneToOneField(Block,on_delete=models.CASCADE,related_name='dist')
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    status= models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "Block_allocation"

    def __str__(self):
        return f"{self.user} - {self.block}"





#village model
class village(models.Model):
    name=models.CharField(max_length=50)
    block=models.ForeignKey(Block,on_delete=models.CASCADE,related_name='village')
    status= models.BooleanField(default=True)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "village"

    def __str__(self):
        return self.name



class Programs(models.Model):
    id = models.AutoField(primary_key=True)
    # state=models.ForeignKey(State,on_delete=models.CASCADE)
    program_name = models.CharField(max_length=255)
    program_abb=models.CharField(max_length=3)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='programs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "Programs"

    def __str__(self):
	    return self.program_name

class Bulk_File(models.Model):
    id = models.AutoField(primary_key=True)
    file=models.FileField(upload_to='files', max_length=254)
    name=models.CharField(max_length=50)
    status=models.BooleanField(default=True)
    

    class Meta:
        db_table = "Bulk_Students"

        
class S_Group(models.Model):
    """ Model showcasing the grouped students """
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=30)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "Group"

        
    def __str__(self):
	    return self.group_name
    # def __str__(self):
    #     return "{}: {}".format(self.group_name, self.created_by)


class Mentor(models.Model):
    id= models.AutoField(primary_key=True)
    name= models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    state= models.ForeignKey(State, on_delete=models.CASCADE)
    district= models.ForeignKey(District, on_delete=models.CASCADE)
    block= models.ForeignKey(Block, on_delete=models.CASCADE)
    village=models.ForeignKey(village, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True) 


class Students(models.Model):
    enrollment_id=models.CharField(unique=True,max_length=250,null=True, blank=True)
    gender = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mentor_name  = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    program_id = models.ForeignKey(Programs, on_delete=models.CASCADE,null=True, blank=True,related_name='student')
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_regex = RegexValidator(regex=r'^\+?91?[6-9]\d{9}$', message="Phone number must be entered in the format: '+919999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, unique=True) # Validators should be a list
    status=models.BooleanField(default=False)
    state =models.ForeignKey(State,on_delete=models.CASCADE,related_name='students')
    district =models.ForeignKey(District,on_delete=models.CASCADE,related_name='students')
    block =models.ForeignKey(Block,on_delete=models.CASCADE,related_name='students')
    village_id =models.ForeignKey(village,on_delete=models.CASCADE,related_name='students')
    group_id = models.ForeignKey(S_Group, on_delete=models.CASCADE)
    file_id=models.ForeignKey(Bulk_File,on_delete=models.CASCADE,null=True,blank=True)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Student_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Students"

    def __str__(self):
        return self.first_name

class Group_Student(models.Model):
    id= models.AutoField(primary_key=True)
    group_id = models.ForeignKey(S_Group, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE )
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = ("group_id", "student_id")

        db_table = "Student_Group"

class Work_Allocation(models.Model):
    id= models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE )
    work_detail = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)   

    class Meta:
        db_table = "Work_Allocation"



class UserAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE,related_name='state_user',blank=True,null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,blank=True,null=True)
    block=models.ForeignKey(Block,on_delete=models.CASCADE,related_name='block_user',blank=True,null=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name='A_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "UserAdmin"


from django.db import models
from .models import Programs, State

class ProgramAllocation(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    allocation_date = models.DateField()
    allocation_time = models.TimeField()

    def __str__(self):
        return f"{self.program.program_name} - {self.state.name}"
