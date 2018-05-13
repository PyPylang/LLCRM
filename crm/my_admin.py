from my_admin.site import site
from .models import *
from my_admin.admin_base import BaseAdmin
from django.shortcuts import HttpResponse
class UserProfileAdmin(BaseAdmin):
    list_display=['name','role']
    filter_horizontal=['user_permissions']
class CustomerAdmin(BaseAdmin):
    list_display = ['id','name','source','contact_type','contact','consultant','consult_courses','consult_content','status','date']
    filter_list = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']
    readonly_fields = ['status','consultant']
    filter_horizontal=['consult_courses']
    actions=['Change_status',]
    def Change_status(self,request,obj):
        return HttpResponse('牛逼牛逼牛逼牛逼牛逼牛逼牛逼牛逼牛逼牛逼')
site.register(StudentEnrollment)
site.register(Role)
site.register(CustomerInfo,CustomerAdmin)
site.register(CustomerFollowUp)
site.register(Classlist)
site.register(Branch)
site.register(Courses)
site.register(CourseRecord)
site.register(Student)
site.register(StudyRecord)
site.register(Menus)
site.register(PaymentRecord)
site.register(Contract_template)
site.register(UserProfile,UserProfileAdmin)