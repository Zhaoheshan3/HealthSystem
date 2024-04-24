import json

from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Count
from django.contrib import  messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .forms import LoginForm, ExcelUploadForm, UserInfoForm
from .models import UserInfo, PersonProfile, HealthInfo
from .utils import login_required, admin_required
import pandas as pd

@login_required
def index(request):
    records = HealthInfo.objects.all()

    # 按照 gender 字段进行分类统计
    gender_count_list = []
    gender_count = HealthInfo.objects.values('gender').annotate(count=Count('gender'))
    for item in gender_count:
        gender_count_list.append({"name":item['gender'], 'value':item['count']})

    # 按照 health 字段进行分类统计
    health_count_list = []
    health_count = HealthInfo.objects.values('health').annotate(count=Count('health'))
    for item in health_count:
        health_count_list.append({"name":item['health'], 'value':item['count']})

    # 按照男女，健康状态分别统计

    # 查出health的唯一值
    unique_health_values  = list(HealthInfo.objects.values_list('health', flat=True).distinct())

    # 按性别 分别按照health顺序生成对应的值

    # 男性统计值 - 字典
    gender_health_count_male_dict = {}
    gender_health_count_male_list = []
    gender_health_count_male = HealthInfo.objects.filter(gender='男').values('health').annotate(count=Count('*'))
    for item in gender_health_count_male:
        gender_health_count_male_dict[item['health']] = item['count']

    # 女性统计值 - 字典
    gender_health_count_female_dict = {}
    gender_health_count_female_list = []
    gender_health_count_female = HealthInfo.objects.filter(gender='女').values('health').annotate(count=Count('*'))
    for item in gender_health_count_female:
        gender_health_count_female_dict[item['health']] = item['count']

    #生成最终的list
    for item in unique_health_values:
        gender_health_count_male_list.append(gender_health_count_male_dict.get(item) or 0)
        gender_health_count_female_list.append(gender_health_count_female_dict.get(item) or 0)

    print(gender_health_count_male_list)
    print(gender_health_count_female_list)
    print(list(unique_health_values))

    unhealth_count_list = []
    # 统计总数目
    total_count = HealthInfo.objects.count()
    #统计健康
    health_count = HealthInfo.objects.filter(health='健康').count()

    unhealth_count_list = [{"name":'健康', 'value':health_count}, {"name":'非健康', 'value':total_count - health_count}]
    print(locals())

    return render(request,'index.html', locals())

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = UserInfo.objects.get(username=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['role'] = user.role
                    request.session['username'] = user.username
                    return HttpResponseRedirect(reverse("index"))
                else:
                    messages.error(request, f'密码不正确，请检查后重试!')
            except:
                messages.error(request, f'用户不存在!')
        return render(request, 'login.html', locals())

    form = LoginForm()
    return render(request, 'login.html', locals())

@login_required
def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse("login"))


class UserInfoListView(ListView):
    template_name = 'userinfo.html'
    paginate_by = 15
    def get_queryset(self):
        queryset = UserInfo.objects.all()
        username = self.request.GET.get("username", None)
        role = self.request.GET.get('role', None)

        if username:
            queryset = queryset.filter(username__icontains=username)
        if role:
            queryset = queryset.filter(role__icontains=role)
        return queryset.order_by('id')

@admin_required
def adduser(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                user = UserInfo.objects.filter(username=username).exists()
                if user:
                    messages.error(request, f'用户名已存在，请检查后重试!')
                UserInfo.objects.create(
                    username=username,
                    password=form.cleaned_data['password'],
                    role=form.cleaned_data['role']
                )
            except Exception as e:
                print(e)
                messages.error(request, f'创建出错，请检查后重试!')
                return HttpResponseRedirect(reverse("health:userinfo"))
            messages.success(request, f'系统用户创建成功!')
            return HttpResponseRedirect(reverse("health:userinfo"))
        else:
            messages.error(request, f'创建出错，请检查后重试!')
            return HttpResponseRedirect(reverse("health:userinfo"))

@admin_required
def edituser(request,id):
    user = UserInfo.objects.get(id=id)
    role_list = ['管理员', '教务处','人事处','教师','学生']
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            try:
                user.password=form.cleaned_data['password']
                user.role=form.cleaned_data['role']
                user.save()
            except Exception as e:
                print(e)
            messages.success(request, f'系统用户更新成功!')
            return HttpResponseRedirect(reverse("health:userinfo"))
        else:
            messages.error(request, f'创建出错，请检查后重试!')
            return HttpResponseRedirect(reverse("health:userinfo"))
    else:
        form = UserInfo()
    return render(request,'edituser.html', locals())

@admin_required
def deluser(request,id):
    user = get_object_or_404(UserInfo, pk = id)
    user.delete()
    messages.success(request, '系统用户已删除！')
    return HttpResponseRedirect(reverse('health:userinfo'))

class PersonInfoListView(ListView):
    template_name = 'personinfo.html'
    paginate_by = 15
    def get_queryset(self):
        queryset = PersonProfile.objects.all()

        username = self.request.GET.get("username", None)
        depart = self.request.GET.get("depart", None)
        role = self.request.GET.get('role', None)

        print(username)
        if username:
            queryset = queryset.filter(username__icontains=username)
        if depart:
            queryset = queryset.filter(depart__icontains=depart)
        if role:
            queryset = queryset.filter(role__icontains=role)

        return queryset.order_by('create_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        context['query_string'] = query_params.urlencode()
        context['username'] = query_params.get('username', '')
        context['depart'] = query_params.get('depart', '')
        context['role'] = query_params.get('role', '')
        return context

@admin_required
def upload_personinfo_xls(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取上传的文件
            file = request.FILES['xlsfile']
            # 使用 pandas 解析 Excel 文件
            df = pd.read_excel(file)
            # 将数据保存到数据库
            try:
                for _, row in df.iterrows():
                    try:
                        PersonProfile.objects.update_or_create(
                            username=row.iloc[0],
                            id_num=row.iloc[2],
                            defaults={
                                'num' : row.iloc[1],
                                'depart' : row.iloc[3],
                                'role' : row.iloc[4]
                            }
                        )
                    except Exception as e:
                        print(e)
                        continue
            except Exception as e:
                print(e)
                messages.error(request, f'excel数据不符合要求，请检查后重试!')
                return HttpResponseRedirect(reverse("health:personinfo"))
            messages.success(request, f'导入excel数据成功!')
            return HttpResponseRedirect(reverse("health:personinfo"))
        else:
            messages.error(request, f'excel数据不符合要求，请检查后重试!')
            return HttpResponseRedirect(reverse("health:personinfo"))

@login_required
def delperson(request,id):
    person = get_object_or_404(PersonProfile, pk = id)
    person.delete()
    messages.success(request, '人员已删除！')
    return HttpResponseRedirect(reverse('health:personinfo'))

class HealthInfoListView(ListView):
    template_name = 'healthinfo.html'
    paginate_by = 15
    
    def get_queryset(self):
        role = self.request.session.get('role')

        queryset = HealthInfo.objects.all()
        username = self.request.GET.get("username", None)
        gender = self.request.GET.get("gender", None)
        health = self.request.GET.get('health', None)
        depart = self.request.GET.get('depart', None)

        if role == '人事处':
            queryset = queryset.exclude(personinfo__depart__in=['教务处','管理员'])
        elif role == '教师':
            queryset = queryset.exclude(personinfo__depart__in=['人事处','教务处','管理员'])

        if username:
            queryset = queryset.filter(personinfo__username__icontains=username)
        if gender:
            queryset = queryset.filter(gender__icontains=gender)
        if health:
            queryset = queryset.filter(health__icontains=health)
        if depart:
            queryset = queryset.filter(personinfo__depart__icontains=depart)

        return queryset.order_by('create_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        context['query_string'] = query_params.urlencode()
        context['username'] = query_params.get('username', '')
        context['gender'] = query_params.get('gender', '')
        context['health'] = query_params.get('health', '')
        context['depart'] = query_params.get('depart', '')
        return context

@admin_required
def upload_healthinfo_xls(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取上传的文件
            file = request.FILES['xlsfile']
            # 使用 pandas 解析 Excel 文件
            df = pd.read_excel(file)
            # 将数据保存到数据库
            try:
                for _, row in df.iterrows():
                    try:
                        username=row.iloc[0]
                        id_num=row.iloc[2]
                        user = PersonProfile.objects.filter(id_num=id_num).first()
                        if user:
                            HealthInfo.objects.update_or_create(
                                personinfo = user,
                                defaults={
                                    'gender': row.iloc[1],
                                    'health': row.iloc[3]
                                }
                            )
                        else:
                            print(f'{username} 不存在校园名单中!')
                    except Exception as e:
                        print(e)
                        continue
            except Exception as e:
                print(e)
                messages.error(request, f'excel数据不符合要求，请检查后重试!')
                return HttpResponseRedirect(reverse("health:healthinfo"))
            messages.success(request, f'导入excel数据成功!')
            return HttpResponseRedirect(reverse("health:healthinfo"))
        else:
            messages.error(request, f'excel数据不符合要求，请检查后重试!')
            return HttpResponseRedirect(reverse("health:healthinfo"))



@login_required
def edithealth(request,id):
    record = HealthInfo.objects.get(id=id)
    if request.method == 'POST':
        try:
            record.health=request.POST.get('health')
            record.comment=request.POST.get('comment')
            record.save()
        except Exception as e:
            print(e)
        messages.success(request, f'更新成功!')
        return HttpResponseRedirect(reverse("health:healthinfo"))

    else:
        return render(request,'edithealth.html', locals())

@admin_required
def delhealth(request,id):
    health = get_object_or_404(HealthInfo, pk = id)
    health.delete()
    messages.success(request, '健康信息已删除！')
    return HttpResponseRedirect(reverse('health:healthinfo'))

def handle_404(request):
    return render(request, '404.html')

def handle_500(request):
    return render(request, '500.html')



