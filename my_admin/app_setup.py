
from django import conf
def admin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            __import__('%s.my_admin'%app_name)
        except ImportError:
            pass