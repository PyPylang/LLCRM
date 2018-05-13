from django import forms
from django.forms import fields, widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core.validators import RegexValidator

class Userform(forms.Form):
    email = forms.EmailField(
            label='邮箱',
            label_suffix=':',
            max_length=18,
            min_length=2,
            required=True,
            error_messages={
                'required': '邮箱不能为空',
            },
            widget=widgets.TextInput(attrs={'class': "form-control"})
    )
    name = forms.CharField(
            label='用户名',
            label_suffix=':',
            max_length=18,
            min_length=2,
            required=True,
            error_messages={
                'required': '用户名不能为空',
                'max_length': '用户名太长了',
                'min_length': '用户名太短了',
            },
            widget=widgets.TextInput(attrs={'class': "form-control"})
    )
    password = forms.CharField(
            required=True,
            min_length=8,
            max_length=32,
            validators=[RegexValidator(
                    r'^(?![a-zA-z]+$)(?!\d+$)(?![!@#$%^&*]+$)[a-zA-Z\d!@#$%^&*]+$',
                    '密码必须包含字母和数字或特殊字符',
            ),],
            error_messages={
                'required': '密码不能为空',
                'min_length': '密码太短',
                'max_length': '密码太长',
            },
            widget=widgets.TextInput(attrs={ 'type':'password','class': "form-control"})

    )


    password2 = forms.CharField(
            required=True,
            min_length=8,
            max_length=32,
            validators=[RegexValidator(
                    '^(?![a-zA-z]+$)(?!\d+$)(?![!@#$%^&*]+$)[a-zA-Z\d!@#$%^&*]+$',
                    '密码必须包含字母和数字或特殊字符',
            ),],
            error_messages={
                'required': '密码不能为空',
                'min_length': '密码太短',
                'max_length': '密码太长',
            },
            widget=widgets.TextInput(attrs={'type':'password','class': "form-control"})

    )
    img = forms.FileField(
        label='头像',
        label_suffix=':',
        required=True,
        error_messages={
            'required': '请上传头像',
        },
        widget=widgets.FileInput(attrs={'id':'put_img', 'style': "opacity: 0;"})
    )

    def clean(self):
        value_dict = self.cleaned_data
        p1 = value_dict.get('password')
        p2 = value_dict.get('password2')
        if p1 != p2:
            raise ValidationError('两次密码不一致！')
        else:
            return self.cleaned_data
