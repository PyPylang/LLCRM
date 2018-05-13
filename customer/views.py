from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm import models
@login_required
def show(request,*args,**kwargs):
    ret = {}
    menus=models.Menus.objects.all()
    ret['menus']=menus
    # 测试千万别用request.session['username']
    # 测试用customer_id=5
    enrollment_objs=models.StudentEnrollment.objects.filter(customer_id=5)
    ret['enrollment_objs']=list(set(enrollment_objs))
    return render(request,'customer/customer.html',ret)