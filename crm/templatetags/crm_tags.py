from django.template import Library
from django.utils.safestring import mark_safe
import datetime, time,json
from crm import models
register=Library()
@register.simple_tag
def format(enrollment_obj,field_name,exmp):
    data_field=enrollment_obj._meta.get_field(field_name)
    if not exmp:
        y="""<i class="fa fa-times-circle" style="color:red"></i>"""
        return mark_safe(y)
    else:
        if data_field.get_internal_type()=='NullBooleanField':
            if exmp == True:
                y="""<i class='fa fa-check-circle' style="color:green"></i>"""
                return mark_safe(y)
        elif data_field.get_internal_type()=="DateTimeField":
            return "%s年%s月%s日"%(exmp.year,exmp.month,exmp.day)
        else:
            return exmp
@register.simple_tag
def customer_info(customer_obj,disabled_field):
    ele=''
    for info in disabled_field:
        info_obj = customer_obj._meta.get_field(info)
        if info_obj.choices:
            mess = getattr(customer_obj, 'get_%s_display' % info)()
            p="<div class='info'><b>%s: </b><b>%s</b></div>"%(info,mess)
            ele+=p
        elif info_obj.get_internal_type()=='ManyToManyField':
            consult_courses=models.Courses.objects.filter(customerinfo=customer_obj)
            p="<div class='info'><b>咨询的产品: </b>"
            c=''
            for course in consult_courses:
                c+='<b>%s </b>'%(course)
            p=p+c+'</div>'
            ele+=p
        else:
            mess=getattr(customer_obj,info)
            p="<div class='info'><b>%s: </b><b>%s</b></div>"%(info,mess)
            ele+=p
    return mark_safe(ele)
@register.simple_tag
def customer(username):
    ele=''
    user=models.UserProfile.objects.filter(name=username).first()
    customers=models.CustomerInfo.objects.filter(consultant__role__userprofile=user)
    customers=list(set(customers))
    for customer in customers:
        op="<option  value=%s>%s</option>"%(customer.id,customer.name)
        ele+=op
    return mark_safe(ele)
@register.simple_tag
def classlist():
    ele=''
    classlists=models.Classlist.objects.all()
    for classlist in classlists:
        name="%s(%s)期" %(classlist.course.name,classlist.semester)
        op="<option  value=%s>%s</option>"%(classlist.id,name)
        ele+=op
    return mark_safe(ele)