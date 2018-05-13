from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$',views.index,name='index'),
    re_path(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/$',
            views.table_obj_list, name="table_obj_list"),
    re_path(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/add/$',
            views.table_obj_add, name="table_obj_add"),
    re_path(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<id>\d+)/change/$',
            views.table_obj_change, name="table_obj_change"),
    re_path(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<id>\d+)/delete/$',
            views.table_obj_delete, name="table_obj_delete"),
    re_path(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/multiple_delete/$',
            views.table_multiple_delete, name="table_multiple_delete"),
]
app_name='my_admin'