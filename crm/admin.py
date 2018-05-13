from django.contrib import admin
from .models import *
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','name','source','contact_type','contact','consultant','consult_content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']
    readonly_fields = ['status','consultant']
    filter_horizontal=['consult_courses']
admin.site.register(CustomerInfo,CustomerAdmin)
admin.site.register(UserProfile)
admin.site.register(Role)
admin.site.register(StudentEnrollment)
admin.site.register(CustomerFollowUp)
admin.site.register(Classlist)
admin.site.register(Branch)
admin.site.register(Courses)
admin.site.register(CourseRecord)
admin.site.register(Student)
admin.site.register(StudyRecord)
admin.site.register(Menus)


