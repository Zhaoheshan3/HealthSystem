from django.db import models


class UserInfo(models.Model):   
    username = models.CharField('用户名',unique=True , max_length=20)
    password = models.CharField('密码',max_length=20)
    role = models.CharField('角色', max_length = 20)
    def __str__(self):
        return f'{self.username}'

class PersonProfile(models.Model): 
    username = models.CharField('用户名',max_length=20)
    num = models.CharField('工号', max_length=10)
    id_num = models.CharField('身份证号', unique=True ,  max_length=30)
    depart = models.CharField('部门', max_length=30)
    role = models.CharField('身份', max_length=20)
    create_time = models.DateTimeField('申请时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.username

class HealthInfo(models.Model): 
    personinfo =  models.OneToOneField(PersonProfile, on_delete=models.CASCADE)
    gender = models.CharField('性别', max_length=10)
    health = models.CharField('症状', max_length=20)
    comment =  models.CharField('备注', null=True, blank=True,  max_length=200,default='无')
    create_time = models.DateTimeField('申请时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    # def __str__(self):
    #     return self.username
