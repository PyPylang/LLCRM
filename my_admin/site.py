from my_admin import admin_base
class AdminSite(object):
    def __init__(self):
        self.enabled_admin={}
    def register(self,model_class,admin_class=None):
        app_name=model_class._meta.app_label
        model_name=model_class._meta.model_name
        print(model_name)
        # 判断别名
        if model_class._meta.verbose_name_plural:
            model_name=model_class._meta.verbose_name_plural
        if not admin_class:
             admin_class=admin_base.BaseAdmin()  #()变成一个实例
        else:
            admin_class=admin_class()
        admin_class.model=model_class
        if app_name not in self.enabled_admin:
            self.enabled_admin[app_name]={}
        self.enabled_admin[app_name][model_name]=admin_class
site=AdminSite()
# enabled_admin={
#     app_name:{model_name:admin_class,model_name:admin_class},
#     app_name:{model_name:admin_class,model_name:admin_class},
# }
