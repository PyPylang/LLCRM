from django.shortcuts import render,HttpResponse,redirect
from .check_code import create_validate_code
from io import BytesIO
from crm import models
import json
import uuid
import os
from .form import Userform
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout,authenticate
def get_code_img(request):
    img,code=create_validate_code()
    stream=BytesIO()
    img.save(stream,"PNG")
    request.session['checkcode']=code
    return HttpResponse(stream.getvalue())
@csrf_exempt
def get_user_img(request):
    ret={'status':'Y','path':None,'msg':None}
    obj=request.FILES.get('k3')
    nid=str(uuid.uuid4())
    file_path=os.path.join('static','img','pre_user_img',nid+obj.name)
    f=open(file_path,'wb')
    for line in obj.chunks():
        f.write(line)
    f.close()
    ret['path']=file_path
    return HttpResponse(json.dumps(ret))
@csrf_exempt
def my_login(request):
    ret = {'status': False, 'data': None, 'msg': None,'code_check':None,'user_site':None}
    username = request.POST.get('username')
    password = request.POST.get('password')
    # #获取验证码
    input_code=request.POST.get('code').upper()
    check_code=request.session['checkcode'].upper()
    if input_code==check_code:
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            ret['status'] = True
            # 设置登录session保存时间
            if request.POST.get('rmb')=='choices':
                request.session.set_expiry(60*60*24*30)
            request.session["username"] = user.name
            request.session["img"] =  str(user.img)
        else:
            ret['msg'] = '用户不存在或密码错误！'
        return HttpResponse(json.dumps(ret))
    else:
        ret['code_check']='验证码错误!'
        return HttpResponse(json.dumps(ret))
def my_register(request):
    if request.method != 'POST':
        form = Userform()
        ret = {'form': form}
        return render(request, 'register.html', ret)
    else:
        form = Userform(request.POST, request.FILES)
        ret = {'form': form,'code':None}
        # 验证验证码
        input_code=request.POST.get('code').upper()
        check_code=request.session['checkcode'].upper()
        if input_code==check_code:
            if form.is_valid():
                del form.cleaned_data['password2']
        # 调用create_user方法给密码加密
                models.UserProfile.objects.create_user(
                        **form.cleaned_data
                )

                # 设置session自动登录
                new_username=request.POST.get('name')
                request.session["username"] = new_username
                request.session["img"] =  str(models.UserProfile.objects.filter(name=new_username).first().img)
                return redirect('/index/')
            else:
                return render(request, 'register.html', ret)
        else:
            ret['code']='验证码错误!'
            return render(request, 'register.html', ret)
def my_logout(request):
    del request.session['username']
    del request.session['img']
    return redirect('/index/')

def index(request):
    return render(request,'backend_base.html')