from django.contrib import admin
from .models import State, District, Block, Village, Program, Student



admin.site.register(State)
admin.site.register(District)
admin.site.register(Block)
admin.site.register(Village)
admin.site.register(Program)
admin.site.register(Student)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'program', 'village', 'block', 'district', 'state')
    list_filter = ('program', 'village__block__district__state')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(village__block__district__state=request.user.state)
        return qs




