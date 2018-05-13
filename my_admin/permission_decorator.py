
from django.shortcuts import render
from my_admin.permission_list import permission_dict
from django.urls import resolve
# permission_dict={
#     'crm_table_list':['table_obj_list','GET',[],{}],
#     'crm_table_list_view':['table_obj_change','GET',[],{}],
#     'crm_table_list_change':['table_obj_change','POST',[],{}],
#     'crm_table_obj_add_view':['table_obj_add','GET',[],{}],
#     'crm_table_obj_add':['table_obj_add','POST',[],{}],
#     'crm_view_own_customers':['table_obj_list','GET',[],{},
#                                  permission_hook.only_view_own_customers],
# }
def perm_check(*args,**kwargs):
    request=args[0]
    url_name=resolve(request.path).url_name
    match_results=[None,]
    match_key=None
    # print(request.user)
    # table_obj_list
    # 李浪
    # print(request.user.is_authenticated())
    # if  request.user.is_authenticated():
    #     return redirect('/index/')
    for permission_key,permission_val in permission_dict.items():
        # 把权限字典解析出来
        perm_name=permission_val[0]
        perm_method=permission_val[1]
        perm_args=permission_val[2]
        perm_kwagrs=permission_val[3]
        perm_hook_func=permission_val[4] if len(permission_val)>4 else None
        # print(perm_name,perm_method,perm_args,perm_kwagrs,perm_hook_func)
        #table_obj_add ['GET'] [] {}
        # 第一个权限都没有直接False
        print(url_name,perm_name)
        if url_name == perm_name:
            print('ss-------')
            # 逐个参数匹配
            # print(request.method)
            if request.method == perm_method:
                # 匹配参数
                args_matched = False
                for arg in perm_args:
                    # 判断request字典中是否有此参数
                    request_method_func=getattr(request,perm_method)
                    print(request_method_func)
                    if request_method_func.get(arg,default=None):
                        args_matched = True
                    else:
                        args_matched = False
                        break
                # 为空时也为True
                else:
                    args_matched=True
                kargs_matched=False
                for k,v in perm_kwagrs.items():
                    request_method_func=getattr(request,perm_method)
                    request_key=request_method_func.get(k,default=None)
                    if request_key==v:
                        kargs_matched=True
                    else:
                        kargs_matched=False
                # 为空时也为True
                else:
                    kargs_matched=True
                perm_func_matched = False
                if perm_hook_func:
                    if  perm_hook_func(request,args,kwargs):
                        perm_func_matched = True

                    else:
                        perm_func_matched = False
                # 为空时也为真
                else:
                    perm_func_matched = True
                match_results = [args_matched,kargs_matched,perm_func_matched]
                print(match_results)
                #都匹配上all()方法
        # 下面的match_key别放错了啊，要等于匹配完的那个permission_key
        if all(match_results):
            match_key = permission_key
            break
    if all(match_results):
        app_name, *per_name = match_key.split('_')
        # print(app_name, *per_name)
        perm_obj = '%s.%s' % (app_name,match_key)

        print(perm_obj)
        # crm.crm_index
        if request.user.has_perm(perm_obj):
            print('当前用户有此权限')
            return True
        else:
            print('当前用户没有该权限')
            return False
            # 这个else即当请求的url_name都不匹配时
    else:
        print("未匹配到任何权限项，当前用户无权限")
        # return False

def check_permission(func):
    def inner(*args,**kwargs):
        if not perm_check(*args,**kwargs):
            request = args[0]
            return render(request,'my_admin/page_403.html')
        return func(*args,**kwargs)
    return  inner
