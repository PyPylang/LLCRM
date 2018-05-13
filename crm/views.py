from django.shortcuts import render, HttpResponse
from . import models
from .form import CustomerInfo
import os, json
from datetime import datetime
from django import conf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def show(request, *args, **kwargs):
    ret = {}
    menus=models.Menus.objects.all()
    ret['menus']=menus
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        classlist_id = request.POST.get('classlist_id')
        user = models.UserProfile.objects.filter(name=request.session['username']).first()
        enrollment_obj = models.StudentEnrollment.objects.create(
                customer_id=customer_id,
                class_grade_id=classlist_id,
                consultant_id=user.userprofile.id,

        )
        enrollment_link = 'http://127.0.0.1:8001/sale/enrollment/%s/' % customer_id
        enrollment_obj.link = enrollment_link,
        ret['link'] = enrollment_obj.link
        ret['customer_id'] = customer_id
    userprofile=models.UserProfile.objects.filter(name=request.session['username']).first()
    enrollment_objs=models.StudentEnrollment.objects.filter(consultant__role__userprofile=userprofile)
    ret['enrollment_objs']=list(set(enrollment_objs))
    return render(request, 'crm/sale.html', ret)


def enrollment(request, *args, **kwargs):
    ret = {}
    customer_id = kwargs['customer_id']
    customer_obj = models.CustomerInfo.objects.filter(id=customer_id).first()
    enrollment_obj = models.StudentEnrollment.objects.filter(customer_id=customer_id).first()
    ret['enrollment_id'] = enrollment_obj.id
    customer_form = CustomerInfo
    ret['form'] = customer_form
    classlist_obj = models.Classlist.objects.filter(studentenrollment__customer=customer_obj).first()
    ret['contract_template'] = classlist_obj.contract_template
    ret['customer_obj'] = customer_obj
    ret['disabled_field'] = customer_form.disabled_field
    # 列出已上传文件
    uploaded_files = []
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR, str(enrollment_obj.id))
    if os.path.isdir(enrollment_upload_dir):
        uploaded_files = os.listdir(enrollment_upload_dir)
        ret['uploaded_files'] = uploaded_files

    if request.method == "POST":
        form = CustomerInfo(request.POST)
        if form.is_valid():
            customer_obj.company = request.POST.get('company'),
            customer_obj.id_num = request.POST.get('id_num')

            enrollment_obj.contract_agreed = True
            enrollment_obj.contract_signed_date = datetime.now()
            enrollment_obj.save()
            return HttpResponse("您已成功提交信息,请等待审核通过!")

    return render(request, 'crm/enrollment.html', ret)


@csrf_exempt
def enrollment_fileupload(request, *args, **kwargs):
    # print(request.FILES)
    enrollment_id = kwargs['enrollment_id']
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR, enrollment_id)
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)
    file_obj = request.FILES.get('file')
    if len(os.listdir(enrollment_upload_dir)) <= 2:
        with open(os.path.join(enrollment_upload_dir, file_obj.name), "wb") as f:
            for chunks in file_obj.chunks():
                f.write(chunks)
    else:
        return HttpResponse(json.dumps({'status': False, 'err_msg': 'max upload limit is 2'}))
    return HttpResponse(json.dumps({'status': True,}))
