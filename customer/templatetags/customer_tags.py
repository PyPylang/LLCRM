
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
def customer_link(username):
    # 测试用customer_id
    customer_id=5
    enrollment_link='/sale/enrollment/%s/'%customer_id
    return enrollment_link