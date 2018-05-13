



# hook自己测试用的，因为还没写带有查自己顾客的url所以全返回True
def only_view_own_customers(request,*args,**kwargs):
    if str(request.user.id) == request.GET.get('consultant'):
        return True
    else:
        return True