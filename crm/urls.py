from django.urls import re_path
from . import views
urlpatterns = [

    re_path(r'^$',views.show,name='show'),
    re_path(r'^enrollment/(?P<customer_id>\d+)/$',views.enrollment,name='enrollment'),
    re_path(r'^enrollment/(?P<enrollment_id>\d+)/fileupload/$', views.enrollment_fileupload,name="enrollment_fileupload"   ),

]
app_name='crm'