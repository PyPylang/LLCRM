# Generated by Django 2.0.2 on 2018-05-04 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20180426_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract_template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('data', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=100, verbose_name='价钱(万元)')),
                ('date', models.DateTimeField()),
                ('pyment_type', models.IntegerField(choices=[(0, '首付款'), (1, '全款')])),
                ('consultant', models.ForeignKey(on_delete=False, to='crm.UserProfile')),
                ('enrollment', models.ForeignKey(on_delete=False, to='crm.StudyRecord')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_agreed', models.BooleanField(default=False)),
                ('contract_approved', models.BooleanField(default=False)),
                ('contract_signed_date', models.DateTimeField()),
                ('contract_approved_date', models.DateTimeField()),
                ('class_grade', models.ForeignKey(on_delete=False, to='crm.Classlist')),
                ('consultant', models.ForeignKey(on_delete=False, to='crm.UserProfile')),
                ('custamer', models.ForeignKey(on_delete=False, to='crm.CustomerInfo')),
            ],
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract_template',
            field=models.ForeignKey(default=2009, on_delete=False, to='crm.Contract_template'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='studentenrollment',
            unique_together={('custamer', 'class_grade')},
        ),
    ]
