# Generated by Django 2.0.2 on 2018-05-06 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0022_auto_20180506_1954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('crm_table_list', '可以查看mydmin每张表里所有的数据'), ('crm_table_list_view', '可以访问mydmin表里每条数据的修改页'), ('crm_table_list_change', '可以对mydmin表里的每条数据进行修改'), ('crm_table_obj_add_view', '可以访问mydmin每张表的数据增加页'), ('crm_table_obj_add', '可以对mydmin每张表进行数据添加')), 'verbose_name_plural': '用户信息'},
        ),
    ]