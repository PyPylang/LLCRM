"""LLCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^index/$',views.index,name='login_index'),
    re_path(r'^sale/',include('crm.urls',namespace='crm')),
    re_path(r'^customer/',include('customer.urls',namespace='customer')),
    re_path(r'^myadmin/',include('my_admin.urls',namespace='my_admin')),
    re_path(r'^login/$',views.my_login,name='login'),
    re_path(r'^logout/$',views.my_logout,name='logout'),
    re_path(r'^register/$',views.my_register,name='register'),
    re_path(r'^get_code_img/$',views.get_code_img,name='get_code_img'),
    re_path(r'^get_user_img/$',views.get_user_img,name='get_user_img'),

]
