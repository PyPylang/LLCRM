from my_admin.site import site
from customer import models


class TestAdmin(object):
    list_display = ['name']

site.register(models.Test,TestAdmin)