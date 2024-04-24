
from django import forms
from .models import UserInfo

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=20)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     filter_result = UserInfo.objects.filter(username__exact=username)
    #     if not filter_result:
    #         raise forms.ValidationError("用户不存在！")
    #     return username

class ExcelUploadForm(forms.Form):
    xlsfile = forms.FileField()


class UserInfoForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=20)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    role = forms.CharField(label='角色')

# class EditUserInfoForm(forms.ModelForm):
    # class Meta:
    #     model = UserInfo
        # fields = ['gender', 'birth']
        # widgets = {
        #     'birth': SelectDateWidget(years=range(1930, 2010), attrs={'style': 'display: inline-block; width: 15%;margin-right:5px'})
        # }