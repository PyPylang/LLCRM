from django import forms
from django.forms import fields, widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core.validators import RegexValidator

class CustomerInfo(forms.Form):
    disabled_field=['name','status','contact','consult_courses','consultant']
    company = forms.CharField(
            label='所在公司',
            label_suffix=':',
            max_length=18,
            min_length=2,
            required=True,
            error_messages={
                'required': '公司名不能为空',
                'max_length': '公司名太长了',
                'min_length': '公司名太短了',
            },
            widget=widgets.TextInput(attrs={'class': "form-control"})
    )
    id_num = forms.CharField(
            label='身份证',
            required=True,
            min_length=8,
            max_length=32,
            validators=[RegexValidator(
                    r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',
                    '非法身份证号码',
            ),],
            error_messages={
                'required': '身份证号码不能为空',

            },
            widget=widgets.TextInput(attrs={ 'class': "form-control"})

    )
