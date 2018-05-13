from django.urls import re_path
from . import views
urlpatterns = [

    re_path(r'^$',views.show,name='show'),

]
app_name='customer'