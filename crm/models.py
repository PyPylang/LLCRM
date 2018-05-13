from django.db import models

# Create your models here.
#
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None, img=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('需要一个合法的邮箱地址')

        user = self.model(
                email=self.normalize_email(email),
                name=name,
                img=img,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
                email,
                password=password,
                name=name,

        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
            verbose_name='邮箱地址',
            max_length=255,
            unique=True,

    )
    # 然后就可以随意扩展字段
    name = models.CharField(max_length=64, verbose_name="姓名")
    img = models.ImageField(upload_to='static/img/UserProfile', verbose_name='头像')
    is_active = models.BooleanField(default=True,verbose_name='启用账号')
    is_staff = models.BooleanField(default=True,verbose_name='设为管理员')
    role = models.ManyToManyField("Role", blank=True, null=True,verbose_name='角色')

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = '用户信息'
        permissions = (
            ('crm_index','访问mydmin首页'),
            ('crm_table_list', '查看mydmin每张表里所有的数据'),
            ('crm_table_change_view', '访问mydmin表里每条数据的修改页'),
            ('crm_table_change_action', '对mydmin表里的每条数据进行修改'),
            ('crm_table_add_view', '访问mydmin每张表的数据增加页'),
            ('crm_table_add_action', '对mydmin每张表进行数据添加'),
            ('crm_view_own_customers','在mydmin客户管理只能查看自己的客户'),
            ('crm_table_delete_view','访问mydmin的删除页'),
            ('crm_table_delete_action','执行mydmin的删除页'),
            ('crm_table_multiple_delete_view','访问action的批量删除页'),
            ('crm_table_multiple_delete_action','执行action的批量删除页'),
        )


# http://127.0.0.1:8080/myadmin/
# class Users(models.Model):
#     username = models.CharField(max_length=30)
#     password = models.CharField(max_length=30)
#     img = models.ImageField(upload_to='static/img/users')
#
#     class Meta:
#         verbose_name_plural = "用户"
#
#     def __str__(self):
#         return self.username

#
# class UserProfile(models.Model):
#     """用户信息表"""
#     user = models.OneToOneField('Users', on_delete=False)
#     name = models.CharField(max_length=64, verbose_name="姓名")
#     role = models.ManyToManyField("Role", blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = '用户信息'


class Role(models.Model):
    name = models.CharField(max_length=200)
    menus = models.ManyToManyField('Menus')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '角色'


class Menus(models.Model):
    name = models.CharField(max_length=200)
    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic'),
    )
    url_type = models.SmallIntegerField(choices=url_type_choices)
    url_name = models.CharField(max_length=300)

    class Meta:
        unique_together = ('name', 'url_name')
        verbose_name_plural = '菜单'

    def __str__(self):
        return self.name + self.url_name


class CustomerInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name='姓名')
    company = models.CharField(max_length=100, null=True, verbose_name='所属公司')
    id_num = models.IntegerField(null=True, verbose_name='身份证')
    status_choices = (
        (0, '未合作'),
        (1, '已合作'),
    )
    status = models.SmallIntegerField(choices=status_choices, verbose_name='合作状态')
    contact_type_choices = (
        (0, 'QQ'),
        (1, '微信'),
        (2, '手机'),
    )
    contact_type = models.SmallIntegerField(choices=contact_type_choices, verbose_name='联系类型')
    contact = models.CharField(max_length=200, verbose_name='联系方式')
    consult_courses = models.ManyToManyField('Courses', verbose_name='意向产品')
    consult_content = models.TextField(max_length=500, verbose_name='合作事宜')
    date = models.DateField(auto_now_add=True, verbose_name='合作日期')
    consultant = models.ForeignKey('UserProfile', on_delete=False, verbose_name='商议人（销售）')
    source_choices = (
        (0, '网站宣传'),
        (1, '高校合作'),
        (2, '企业合作'),
        (3, '线下广告'),
    )
    source = models.SmallIntegerField(choices=source_choices, verbose_name='来源')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '顾客信息'


class Student(models.Model):
    """学员表"""
    customer = models.ForeignKey("CustomerInfo", on_delete=False)
    class_grades = models.ManyToManyField("Classlist")

    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name_plural = '项目成员信息'


class CustomerFollowUp(models.Model):
    customer = models.ForeignKey('CustomerInfo', on_delete=False)
    content = models.TextField(max_length=500)
    user = models.ForeignKey('UserProfile', on_delete=False)
    status_choices = (
        (0, '近期无购买计划'),
        (1, '一个月内购买'),
    )
    status = models.SmallIntegerField(choices=status_choices)

    def __str__(self):
        return self.content[:50] + '...'

    class Meta:
        verbose_name_plural = '客户跟踪信息'


class Classlist(models.Model):
    """班级列表"""
    branch = models.ForeignKey('Branch', on_delete=False)
    course = models.ForeignKey('Courses', on_delete=False)
    class_type_choices = ((0, '内部项目'), (1, '外部项目'), (2, '国际项目'))
    class_type = models.SmallIntegerField(choices=class_type_choices, default=0)
    semester = models.SmallIntegerField(verbose_name='周期')
    teachers = models.ManyToManyField("UserProfile", verbose_name='总工程师')
    start_date = models.DateField('开工日期')
    graduate_date = models.DateField('竣工日期', blank=True, null=True)

    contract_template = models.ForeignKey('Contract_template', on_delete=False)

    def __str__(self):
        return "%s(%s)期" % (self.course.name, self.semester)

    class Meta:
        unique_together = ('branch', 'class_type', 'course', 'semester')
        verbose_name_plural = '项目'


class Contract_template(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    data = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '合同模板'


class Branch(models.Model):
    """校区"""
    name = models.CharField(max_length=64, unique=True)
    addr = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '工程区域'


class Courses(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    outline = models.CharField(max_length=200)
    period = models.PositiveIntegerField(verbose_name="工程周期(月)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '工程'


class CourseRecord(models.Model):
    class_grade = models.ForeignKey('Classlist', on_delete=False)
    day_num = models.PositiveIntegerField()
    teacher = models.ForeignKey('UserProfile', on_delete=False)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    has_homework = models.BooleanField()
    homework = models.TextField(max_length=1000)
    date = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '工程记录'


class StudyRecord(models.Model):
    course_record = models.ForeignKey("CourseRecord", on_delete=False)
    student = models.ForeignKey("Student", on_delete=False)

    score_choices = ((100, "A+"),
                     (90, "A"),
                     (85, "B+"),
                     (80, "B"),
                     (75, "B-"),
                     (70, "C+"),
                     (60, "C"),
                     (40, "C-"),
                     (-50, "D"),
                     (0, "N/A"),
                     (-100, "COPY"),
                     )
    score = models.SmallIntegerField(choices=score_choices, default=0)
    show_choices = ((0, '缺勤'),
                    (1, '已签到'),
                    (2, '迟到'),
                    (3, '早退'),
                    )
    show_status = models.SmallIntegerField(choices=show_choices, default=1)
    note = models.TextField("绩效备注", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s " % (self.course_record.title, self.date)

    class Meta:
        verbose_name_plural = '工作记录'


class StudentEnrollment(models.Model):
    # 报名表
    customer = models.ForeignKey("CustomerInfo", on_delete=False)
    consultant = models.ForeignKey('UserProfile', on_delete=False)
    class_grade = models.ForeignKey('Classlist', on_delete=False)

    contract_agreed = models.NullBooleanField(default=False)
    contract_approved = models.NullBooleanField(default=False)
    contract_signed_date = models.DateTimeField(null=True)
    contract_approved_date = models.DateTimeField(null=True)

    link = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('customer', 'class_grade')
        verbose_name_plural = '合同'

    def __str__(self):
        return self.customer.name


class PaymentRecord(models.Model):
    # 缴费记录
    enrollment = models.ForeignKey('StudentEnrollment', on_delete=False)
    consultant = models.ForeignKey('UserProfile', on_delete=False)
    amount = models.IntegerField('价钱(万元)', default=100)
    date = models.DateTimeField()
    pyment_type_choices = (
        (0, '首付款'),
        (1, '全款'),
    )
    pyment_type = models.IntegerField(choices=pyment_type_choices)

    def __str__(self):
        return self.enrollment.customer.name

    class Meta:
        verbose_name_plural = '支付记录'
