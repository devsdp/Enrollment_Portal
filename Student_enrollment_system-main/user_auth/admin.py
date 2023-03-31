from django.contrib import admin

from .models import UserAdmin,District,Stateuser,Mentor,Students,Blockuser,Programs,CustomUser,State_allocation,Block_allocation,State,Block,village,S_Group,Group_Student,Bulk_File,Work_Allocation

admin.site.register(CustomUser)
admin.site.register(UserAdmin)
admin.site.register(Stateuser)
admin.site.register(Students)
admin.site.register(Blockuser)
admin.site.register(Programs)
admin.site.register(State)
admin.site.register(State_allocation)
admin.site.register(Block_allocation)
admin.site.register(Block)
admin.site.register(village)
admin.site.register(S_Group)
admin.site.register(Group_Student)
admin.site.register(Bulk_File)
admin.site.register(Work_Allocation)
admin.site.register(Mentor)
admin.site.register(District)