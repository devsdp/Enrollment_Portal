from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .Adminview import Blockusercreate,DistrictCount,Districtcreate,Districtupdate,Villagedataview,Statecreate,Mentorget,BlockCount,Mentorcreate,Mentordetails,Stateallocategetview,Update_All_users,All_users,Stateupdate,All_Student,StudentCount,StateCount,StateGet,Blockcreate,BlockGet,Admincreate,admin_dashboard,AdminGet,Blockcreates,Blockupdateview,GetGroupStudent,Stateusercreate,StudentGroupcreate,Groupget,Groupcreate,Studentcreate,StudentGet,Stateallocateview,allocatedstateupdate,Blockallocateview,AllocatedBlockupdateview,Statecreate
from .Blockuserview import GetstateProgramforclockuser,ProgramListByVillage,GetstateProgram,CreateProgram,StudentList,Block_allocated_datas,StudentCreateAPIView,Block_allocated_data,Programdetailedview,Getallocatedblock,Group_update,Villagecreate,VillageCount,Student_create,Villageupdate,Get_Student,Group_create_B,Bulk_Student_create,Student_update
from .views import Userlogin
from . import views
from user_auth.views import adminhome_dashboard
from .Stateuserview import Blockusercreatebystate,DistrictBlockAPIView,StateDistrictAPIView,ProgramStudentListViews,Get_Student_with_program,Getallocatedstate,StateBlockAPIView,BlockVillagesAPIView,Work_Allocate_get,BlockAllocation,VillageStudentsAPIView,Work_Allocate,Work_Allocate_update,StudentListView,DataModelList,StudentListViews,B_allocateview,BlockStudentListViews

urlpatterns = [
    path('login/', Userlogin.as_view(), name='login'),
    path('logout_user/', views.User_logout, name="logout_user"),
    path('user_create/',Admincreate.as_view(), name="user_create"),
    path('block_user_create/',Blockusercreate.as_view(), name="block_user_create"),
    path('block_user_create_by_state/',Blockusercreatebystate.as_view(), name="block_user_create_by_state"),
    path('mentor_create/',Mentorcreate.as_view(), name="mentor_create"),
    path('Mentor_get/',Mentorget.as_view(), name="Mentor_get"),
    path('Mentor_details/<int:pk>/',Mentordetails.as_view(), name="Mentor_details"),
    path('admin_dashboard/',admin_dashboard.as_view(), name="admin_dashboard"),
    path('All_users/',All_users.as_view(), name="All_users"),
    path('Update_All_users/<int:pk>/',Update_All_users.as_view(), name="Update_All_users"),
    path('all_Admin_get/',AdminGet.as_view(), name="all_Admin_get"),
    #not
    # path('state_user_create/',Stateusercreate.as_view()),
    path('state_user_get/',StateGet.as_view(),name='state_user_get'),
    path('state_create/',Statecreate.as_view(),name='state_create'),
    path('State_update/<int:pk>/',Stateupdate.as_view(), name="State_update"),
    path('state_allocate/',Stateallocateview.as_view(),name='state_allocate'),
    path('state_allocate_list/',Stateallocategetview.as_view(), name="state_allocate_list"),
    path('allocated_state_update/<int:pk>/',allocatedstateupdate.as_view(), name="allocated_state_update"),
    path('Work_Allocate_get/',Work_Allocate_get.as_view(), name="Work_Allocate_get"),
    path('Work_Allocate/',Work_Allocate.as_view(), name="Work_Allocate"),
    path('Work_Allocate_update/<int:pk>/',Work_Allocate_update.as_view(), name="Work_Allocate_update"),
    #old block by admin
    # path('block_user_create/',Blockcreate.as_view()),
    path('create_district/',Districtcreate.as_view(), name="create_district"),
    path('update_district/<int:pk>/',Districtupdate.as_view(), name="update_district"),
    path('block_user_get/',BlockGet.as_view(), name="block_user_get"),
    path('block_create/',Blockcreates.as_view(), name="block_create"),
    path('block_update/<int:pk>/',Blockupdateview.as_view(), name="block_update"),
    path('block_allocate/',Blockallocateview.as_view(), name="block_allocate"),
    path('block_allocation_update/<int:pk>/',AllocatedBlockupdateview.as_view(), name="block_allocation_update"),
    #block user api
    path('create_program/',CreateProgram.as_view(),name='create_program'),
    path('get_allocated_program/',GetstateProgram.as_view(), name="get_allocated_program"),
    path('get_allocated_program_block/',GetstateProgramforclockuser.as_view(), name="get_allocated_program_block"),
    path('villages/<int:village_id>/programs/', ProgramListByVillage.as_view(), name="villages_programs"),
    path('program/<int:pk>/',Programdetailedview.as_view(), name="program"),
    # state user view
    path('state_dashbord/',Getallocatedstate.as_view(), name="state_dashbord"),
    # working on it
    # path('get_s_student/',StudentListView.as_view()),
    #block user view
    path('block_dashbord/',Getallocatedblock.as_view(), name="block_dashbord"),
    #create group and get self created group
    path('Group_create_B/',Group_create_B.as_view(), name="Group_create_B"),
    path('Group_get/<int:pk>/',Group_update.as_view(), name="Group_get"),

    path('village_create/',Villagecreate.as_view(), name="village_create"),
    path('village_data/',Villagedataview.as_view(), name="village_data"),
    path('Village_update/<int:pk>/',Villageupdate.as_view(), name="Village_update"),
    path('student_create/',Student_create.as_view(), name="student_create"),
    path('student_update/<int:pk>/',Student_update.as_view(), name="student_update"),
    path('Bulk_Student_create/',Bulk_Student_create.as_view(), name="Bulk_Student_create"),
    path('get_student/',Get_Student.as_view(), name="get_student"),
    

    # path('create_group/',Groupcreate.as_view()),
    #update self created group delete patch put
    path('group_get/<int:pk>/',Groupget.as_view(), name="group_get"),
    #student adding to created group and get self created group list
    path('Student_create_group/',StudentGroupcreate.as_view(), name="Student_create_group"),
    path('GetGroupStudent/<int:group>/',GetGroupStudent.as_view(), name="GetGroupStudent"),



    #######################################################################################
    
    path('All_state_count/',StateCount.as_view(), name="All_state_count"),
    path('All_district_count/',DistrictCount.as_view(), name="All_district_count"),
    path('All_block_count/',BlockCount.as_view(), name="All_block_count"),
    path('All_village_count/',VillageCount.as_view(), name="All_village_count"),
    path('All_Student_count/',StudentCount.as_view(), name="All_Student_count"),
    path('All_Student/',All_Student.as_view(), name="All_Student"),
    path('block_allocation_user/',B_allocateview.as_view(), name="block_allocation_user"),
    path('block_allocation_list/',BlockAllocation.as_view(), name="block_allocation_list"),
    # path('st_create_all/',StudentCreateAPIView.as_view()),StudentList
    path('students/group/<int:group_id>/',StudentList.as_view(), name="students_group"),

##################################################################################################
#raw Studen_create
    # path('Studen_create/',Studen_create.as_view()),
    path('Studen_get_program/',Get_Student_with_program.as_view(), name="Studen_get_program"),
    path('get_state_data/',DataModelList.as_view(), name="get_state_data"),
    path('block_data/',Block_allocated_data.as_view(), name="block_data"),
    path('block_datas/',Block_allocated_datas.as_view(), name="block_datas"),
    path('states/<int:state_id>/students/', StudentListViews.as_view(), name='state_students'),
    path('block/<int:block_id>/students/', BlockStudentListViews.as_view(), name='block_students'),
    path('program/<int:program_id>/students/', ProgramStudentListViews.as_view(), name='program_students'),
    path('district/<int:district_id>/block/', DistrictBlockAPIView.as_view(), name="district_block"),
    path('block/<int:district_id>/villages/', BlockVillagesAPIView.as_view(), name="block_villages"),
    path('state/<int:state_id>/district/', StateDistrictAPIView.as_view(), name="state_district"),
    path('state/<int:state_id>/Block/', StateBlockAPIView.as_view(), name="state_Block"),
    path('villages/<int:village_id>/students/', VillageStudentsAPIView.as_view(), name="villages_students"),


###############################################################################################

    #####get the path of the templates#########
    path('home',adminhome_dashboard, name="home"),
    # path('block_allocation',views.block_allocation),
    path('block_create',views.block_create, name="block_create"),
    path('block_dashboard',views.block_dasboard, name="Block_dashboard"),
    path('login_user',views.login, name='login_user'),
    path('program',views.program, name="program"),
    path('state_allocation',views.state_allocation, name="state_allocation"),
    path('state_create_data',views.state_create, name="state_create_data"),
    path('state_dasboard',views.state_dasboard, name="State_dasboard"),
    path('user_create',views.user_creat, name="user_create"),
    path('village',views.village, name="village"),
    path('block_allocation',views.block_allocation, name="block_allocation"),
    path('group_view',views.group_view, name="group_view"),
    path('State_Students_view',views.State_Students_view, name="State_Students_view"),
    path('all_user_view',views.all_user_view, name="all_user_view"),
    path('mentor_create_data', views.mentor_create, name="mentor_create_data"),
    path('block_student_view', views.block_student_view, name="block_student_view"),
    path('program_student_view', views.program_student_view, name="program_student_view"),
    path('village_student_view', views.village_student_view, name="village_student_view"),
    path('student_view_data', views.student_view_data, name="student_view_data"),
    path('student_detail/<int:id>', views.student_detail , name='student_detail'),
    path('state_login_admin', views.state_login_admin, name="state_login_admin"),
    path('result_students',views.results, name='results'),
    path('multiple_choice', views.multiple_student_update, name="multiple_choice"),
    path('block_user', views.block_user, name="block_user"),
    


]