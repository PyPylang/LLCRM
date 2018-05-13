from django.template import Library
from django.utils.safestring import mark_safe
import datetime, time,json
from crm import models
register = Library()


# 获取403上一次url
@register.simple_tag
def pre_url(url):
    delete_url, *pre_url = url.split('/')
    # /myadmin/crm/工程记录/4/delete/
    # ['myadmin', 'crm', '菜单', '3', 'delete', '']
    new_url_list=pre_url[0:-3]
    new_url='/'
    for i in new_url_list:
        new_url+=i+'/'
    return new_url
@register.simple_tag
def active_menus(request_path,menu_url_name):
    if menu_url_name in request_path:
        return True
    else:
        return False
@register.simple_tag
def multiple_delete_id(objs):
    ids=[]
    for obj in objs:
        ids.append(obj.id)
    return ids

@register.simple_tag
def display_all_related_obj(obj):
    ele="<ul>"
    for reversed_fk_obj in obj._meta.related_objects:
        related_table_name =  reversed_fk_obj.name
        try:
            related_lookup_key = "%s_set" % related_table_name
        #反向查所有关联的数据

            related_objs = getattr(obj,related_lookup_key).all()
            ele += "<li>%s:<ul> "% related_table_name
 # 总结：ManyToManyField不递归，反向FK递归，OneToOneField没有_set不能迭代
            if reversed_fk_obj.get_internal_type()=='ManyToManyField':
                for i in related_objs:
                    ele+="<li><a href='/myadmin/%s/%s/%s/change/'>%s</a></li>"% (i._meta.app_label,
                                                                     i._meta.model_name,
                                                                     i.id,i,)
            else:
                for i in related_objs:
                    ele+="<li><a href='/myadmin/%s/%s/%s/change/'>%s</a></li>" %(i._meta.app_label,
                                                                            i._meta.model_name,
                                                                            i.id,i)
                    ele+=display_all_related_obj(i)
            ele += "</ul></li>"
            # 哎下面是OneToOneField
        except Exception as e:
            ele += "<li>%s:<ul> "% related_table_name
            related_lookup_key = "%s" % related_table_name
            i = getattr(obj,related_lookup_key)
            ele+="<li><a href='/myadmin/%s/%s/%s/change/'>%s</a></li>"% (i._meta.app_label,
                                                                     i._meta.model_name,
                                                                     i.id,i,)
        ele+="</ul>"
    return mark_safe(ele)


@register.simple_tag
def get_selected_m2m_data_data(form,field,admin_class):
    # 因为add的时候找不到选中的需要判断啊啊啊啊啊啊啊啊啊啊
    if admin_class.form_add:
        return ''
    else:
        selected_data = getattr(form.instance ,field).all()
        return selected_data

@register.simple_tag
def get_available_m2m_data_data(form,field_name,admin_class):

    field_obj = admin_class.model._meta.get_field(field_name)
    # crm.CustomerInfo.consult_courses
    # <class 'crm.models.Courses'>
# "<CustomerInfo: >" needs to have a value for field "id" before this many-to-many relationship can be used.
    obj_list = set(field_obj.related_model.objects.all())
    # 因为add的时候找不到选中的需要判断啊啊啊啊啊啊啊啊啊啊
    if admin_class.form_add:
        return obj_list
    else:
        selected_data = set(getattr(form.instance ,field_name).all())
        return obj_list - selected_data

# 获取只读表单字段名,即具体实例
@register.simple_tag
def get_field_name(admin_class,form,field):
    filed_obj=admin_class.model._meta.get_field(field)
    # print(filed_obj)
    # crm.CustomerInfo.status
    if filed_obj.choices:
        name = getattr(form.instance, 'get_%s_display' % field)()
         # choices的通过split获取字段名然后。。。走弯路了
        # name = getattr(form.instance, 'get_%s_display' % str(filed_obj).split('.', )[-1])()
    else:
        name=getattr(form.instance,field)
    return name
@register.simple_tag
def name_upper(name):
    return name.upper()
# 分页保留过滤
@register.filter
def filter_conditions(filter_conditions):
    if filter_conditions:
        ele=''
        for k,v in filter_conditions.items():
            ele+='&%s=%s'%(k,v)
        return mark_safe(ele)
    else:
        return ''
# 分页保留排序
@register.filter
def order_conditions(sorted_column):
    # print(sorted_column)
    # {'contact_type': '2'}
    if sorted_column:
        ele=''
        for k,v in sorted_column.items():
            ele+='&_o=%s'%(v.strip())
        return mark_safe(ele)
    else:
        return ''
# 分页保留搜索
@register.filter
def search_conditions(search_key):
    if search_key:
        return '&_q=%s'%search_key
    else:
        return ''
# 过滤保留排序
@register.filter
def get_sorted_index(sorted_column):
    if sorted_column:
        ele=''
        for k,v in sorted_column.items():
            if v:
                ele='%s'%v
        return mark_safe(ele)
    else:
        return ''
# 排序保留过滤
@register.filter
def order_filter_conditions(filter_conditions):

    if filter_conditions:
        ele=''
        for k,v in filter_conditions.items():
            ele+='&%s=%s'%(k,v)
        return mark_safe(ele)
    else:
        return ''
# 排序
@register.simple_tag
def get_sorted_column(sorted_column,column,forloop):
    # {'consultant': '4'}
    if column in sorted_column:
        last_order_index=sorted_column[column]
        if last_order_index.startswith('-'):
            return last_order_index.strip('-').strip()
        else:
            return '-%s'%last_order_index
    else:
        return forloop
@register.simple_tag
def get_order_icon(sorted_column,column,):
    if column in sorted_column:
        last_order_index=sorted_column[column]
        if last_order_index.startswith('-'):
            return mark_safe("""<i class="fa fa-caret-down"></i>""")
        else:
            return mark_safe("""<i class="fa fa-caret-up"></i>""")
    else:
        return ''


@register.simple_tag
def build_table_row(obj, admin_class=None):
    ele = ''
    if admin_class.list_display:
        for index,column_name in enumerate(admin_class.list_display):
            column_obj = admin_class.model._meta.get_field(column_name)
            # ManyToMany的还没判断呢傻傻
            if column_obj.choices:
                column_data = getattr(obj, 'get_%s_display' % column_name)()
            elif column_obj.get_internal_type()=="ManyToManyField":
                # 多对多正向查找啊兄弟，搞le这么久
                related_objs= getattr(obj, column_name).all()
                # 先去掉本身名字为空
                column_data=''
                for related_obj in related_objs:
                    column_data+=related_obj.name+'&nbsp;&nbsp;'
            else:
                column_data = getattr(obj, column_name)
                        # 给id列加change
            if index==0:
                td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id,column_data)
            else:
                td_ele = "<td>%s</td>" % column_data
            ele += td_ele
    else:
        ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id,obj)
    return mark_safe(ele)


@register.simple_tag
# filter_list = ['source','consultant','status','date']
def build_filter_row(obj, admin_class):
    filter_column_name = obj
    filter_column_obj = admin_class.model._meta.get_field(filter_column_name)
    all=''
    try:
        if filter_column_obj.get_choices():
            ele = """<select name='%s' class="form-control">""" % filter_column_name
            opp = ""
            for op in filter_column_obj.get_choices():

                if str(op[0])==admin_class.filter_condtions.get(filter_column_name):
                    option = "<option value='%s' selected>%s</option>" % (op[0], op[1])
                else:
                    option = "<option value='%s'>%s</option>" % (op[0], op[1])
                opp += option
            ele = ele + opp + "</select>"
            return mark_safe(ele)
    except AttributeError as e:
        if filter_column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                [time_obj, '今天'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), '本年']
            ]
            # {'status': [''], 'source': ['1'], 'date': ['']}
            ele = """<select name='%s__gte' class="form-control">
            <option value='%s'>-----</option>""" % (filter_column_name,all)
            for i in time_list:
                time_str='%s-%s-%s'%(i[0].year,i[0].month,i[0].day)
                if time_str==admin_class.filter_condtions.get('%s__gte'%filter_column_name):
                    option = "<option value='%s' selected>%s</option>" \
                         % (time_str, i[1])
                else:
                    option = "<option value='%s'>%s</option>" \
                         % (time_str, i[1])
                ele += option
            ele = ele + "</select>"
            return mark_safe(ele)

# column_verbose_name
@register.simple_tag
def column_verbose_name(column,admin_class):
    column_obj=admin_class.model._meta.get_field(column)
    if column_obj.verbose_name:
        return column_obj.verbose_name
    else:
        return column
# 搜索关键字用verbose_name
@register.simple_tag
def search_verbose_name(search_key,admin_class):
    column=search_key.split('__')[0]
    column_obj=admin_class.model._meta.get_field(column)
    if column_obj.verbose_name:
        return column_obj.verbose_name
    else:
        return column
