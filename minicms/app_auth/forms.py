from django import forms


class UserForms(forms.Form):
    """用户表"""
    user_name = forms.CharField(required=True,max_length=32, min_length=3,error_messages={'required': u'必填字段', 'max_length': u'长度超过32位', 'min_length': u'长度太短'})
    ready_name = forms.CharField(required=True, error_messages={'required': u'必填字段'})
    passwd = forms.CharField(required=True, error_messages={'required': u'必填字段'})
    email = forms.EmailField(required=True, error_messages={'required': u'必填字段'})

    # 自定义验证器
    def clean_password(self):
        passwd = self.cleaned_data.get('passwd', None)
        if len(passwd) < 3:
            raise forms.ValidationError(u'密码长度过短', code='min_length')
        return passwd

