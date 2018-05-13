from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from my_admin import app_setup
app_setup.admin_auto_discover()
from my_admin.site import site
from utils import CustomPaginator, my_paginator
from django.db.models import Q
from .form import create_dynamic_model_form
import json
from crm import models
import os
from .permission_decorator import check_permission
# print(site.enabled_admin)
# {'crm': {'users': <my_admin.admin_base.BaseAdmin object at 0x000002944DCD3630>}}
@check_permission
@login_required
def index(request, *args, **kwargs):
    ret = {}
    ret['site'] = site
    menus=models.Menus.objects.all()
    ret['menus']=menus
    return render(request, 'my_admin/index.html', ret)


def get_filter_result(request, querysets):
    filter_condtions = {}
    for k, v in request.GET.items():
        if k in ('_P', '_o', '_q','action'): continue
        if v:
            # 给V去空，让url正常
            filter_condtions[k] = v.strip()
    return querysets.filter(**filter_condtions), filter_condtions


# 搜索
def get_search_result(request, querysets, admin_class):
    search_key = request.GET.get('_q')
    if search_key:
        # search_fields = ['contact','consultant__name']
        q = Q()
        q.connector = 'OR'
        for search_fields in admin_class.search_fields:
            q.children.append( ("%s__contains" %search_fields, search_key))
        return querysets.filter(q),search_key
    else:
        return querysets,search_key


def get_orderby_result(request, querysets, admin_class):
    orderby_index = request.GET.get('_o')
    sorted_column = {}
    if orderby_index:
        orderby_key = admin_class.list_display[abs(int(orderby_index))]
        sorted_column[orderby_key] = orderby_index
        if orderby_index.startswith('-'):
            return querysets.order_by(orderby_key).reverse(), sorted_column
        else:
            return querysets.order_by(orderby_key), sorted_column
    else:
        return querysets, ''

@check_permission
@login_required
def table_obj_list(request, *args, **kwargs):
    ret = {}
    menus=models.Menus.objects.all()
    ret['menus']=menus
    app_name = kwargs['app_name']
    model_name = kwargs['model_name']
    ret['model_name'] = model_name
    admin_class = site.enabled_admin[app_name][model_name]
                            # 动作
    if request.method=='POST':
        import json
        selected_action=request.POST.get('action')
        selected_ids=json.loads(request.POST.get('selected_ids'))
# ['12', '11', '10', '9']
        selected_objs=admin_class.model.objects.filter(id__in=selected_ids)
        action_func=getattr(admin_class,selected_action)
        return action_func(request,selected_objs)



    querysets = admin_class.model.objects.all().order_by('-id')
    # 过滤
    querysets, filter_condtions = get_filter_result(request, querysets)
    # <QueryDict: {'status': [''], 'source': ['1'], 'date': ['']}>
    admin_class.filter_condtions = filter_condtions
    # print(filter_condtions)
    # 搜索
    querysets,search_key = get_search_result(request, querysets, admin_class)
    # 排序
    querysets, sorted_column = get_orderby_result(request, querysets, admin_class)
    # 分页，连函数也可以调用自己以前的函数
    querysets = my_paginator.my_paginator(request, querysets)
    ret['sorted_column'] = sorted_column
    ret['admin_class'] = admin_class
    ret['querysets'] = querysets
    ret['search_key']=search_key
    ret['app_name'] = app_name

    return render(request, 'my_admin/model.html', ret)
@check_permission
@login_required
def table_obj_add(request, *args, **kwargs):
    ret = {}
    menus=models.Menus.objects.all()
    ret['menus']=menus
    app_name = kwargs['app_name']
    model_name = kwargs['model_name']
    ret['model_name'] = model_name
    admin_class = site.enabled_admin[app_name][model_name]
    ret['app_name'] = app_name

    ret['admin_class'] = admin_class

    model_form=create_dynamic_model_form(admin_class,form_add=True)

    if request.method=='GET':
        ret['form']=model_form()
    else:
        form_obj=model_form(request.POST, request.FILES)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/myadmin/%s/%s/'%(app_name,model_name))
    return render(request,'my_admin/table_obj_add.html',ret)
@check_permission
@login_required
def table_obj_change(request, *args, **kwargs):
    ret = {}
    menus=models.Menus.objects.all()
    ret['menus']=menus
    app_name = kwargs['app_name']
    model_name = kwargs['model_name']
    ret['model_name'] = model_name
    admin_class = site.enabled_admin[app_name][model_name]
    ret['app_name'] = app_name
    ret['admin_class'] = admin_class
    model_form=create_dynamic_model_form(admin_class)
    obj=admin_class.model.objects.get(id=kwargs['id'])

    ret['id']=kwargs['id']
    if request.method=='GET':
        form_obj=model_form(instance=obj)
        ret['form']=form_obj
    else:
        form_obj=model_form(request.POST,request.FILES,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/myadmin/%s/%s/'%(app_name,model_name))
    return render(request,'my_admin/table_obj_change.html',ret)

@check_permission
@login_required
def table_obj_delete(request, *args, **kwargs):
    ret = {}
    menus=models.Menus.objects.all()
    ret['menus']=menus
    app_name = kwargs['app_name']
    model_name = kwargs['model_name']
    ret['model_name'] = model_name
    admin_class = site.enabled_admin[app_name][model_name]
    ret['app_name'] = app_name
    ret['admin_class'] = admin_class
    obj=admin_class.model.objects.get(id=kwargs['id'])
    ret['obj']=obj
    ret['id']=kwargs['id']
    if request.method=='POST':
        obj.delete()
        return redirect('/myadmin/%s/%s/'%(app_name,model_name))
    return render(request,'my_admin/table_obj_delete.html',ret)
@check_permission
@login_required
def table_multiple_delete(request, *args, **kwargs):
    if request.method=='POST':
        app_name = kwargs['app_name']
        model_name = kwargs['model_name']
        admin_class = site.enabled_admin[app_name][model_name]
        ids=request.POST.get('multiple_delete')
        for id in json.loads(ids):
            obj=admin_class.model.objects.filter(id=id)
            obj.delete()
        return redirect('/myadmin/%s/%s/'%(app_name,model_name))
