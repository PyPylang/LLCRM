from django.shortcuts import redirect,render
from crm import models


class BaseAdmin(object):
    list_display = []
    filter_list =[]
    search_fields =[]
    readonly_fields = []
    filter_horizontal = []
    actions=[]
    default_actions = ['Delete_selected',]
    def Delete_selected(self,request,objs):
        ret = {}
        menus=models.Menus.objects.all()
        ret['menus'] = menus
        ret['app_name'] = request.POST.get('app_name')
        ret['model_name'] = request.POST.get('model_name')
        ret['objs']=objs
        return render(request,'my_admin/table_objs_delete.html',ret)