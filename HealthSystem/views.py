import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import healthapp
from healthapp.forms import LoginForm, ExcelUploadForm, UserInfoForm
from healthapp.models import UserInfo, PersonProfile, HealthInfo

@csrf_exempt
def addone_person(request):
    if request.method == 'POST':
        try:
            # 从请求体中获取原始数据
            data = json.loads(request.body)

            # 获取表单数据
            username = data.get('username')
            userid = data.get('userid')
            ids = data.get('ids')
            depart = data.get('depart')
            role = data.get('role')

            # 打印获取到的数据
            print('用户名:', username)
            print('学号/工号:', userid)
            print('身份证号:', ids)
            print('部门:', depart)
            print('身份:', role)

            # 创建 PersonProfile 实例并保存数据
            person = PersonProfile.objects.create(
                username=username,
                num=userid,
                id_num=ids,
                depart=depart,
                role=role
            )
            # 返回成功响应
            return HttpResponse("添加成功")

        except json.JSONDecodeError:
            return JsonResponse({'error': '无法解析JSON数据'}, status=400)

    # 如果请求方法不是POST，返回错误响应
    return HttpResponse("只允许POST请求")

@csrf_exempt
def search_person_by_name(request, name):
    if request.method == 'GET':
        # 使用 filter 方法根据姓名查询数据库中的数据
        persons = PersonProfile.objects.filter(username=name)

        # 将查询到的数据序列化为JSON格式并返回给前端
        data = []
        for person in persons:
            data.append({
                'id': person.id,
                'username': person.username,
                'num': person.num,
                'id_num': person.id_num,
                'depart': person.depart,
                'role': person.role,
                'create_time': person.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': person.update_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse(data, safe=False)

    # 如果请求方法不是GET，返回错误响应
    return JsonResponse({'error': '只允许GET请求'}, status=400)


@csrf_exempt
def addone_healthy(request):
    if request.method == 'POST':
        try:
            # 从请求体中获取原始数据
            data = json.loads(request.body)

            # 获取表单数据
            username = data.get('username')
            gender = data.get('gender')
            ids = data.get('ids')
            healthy = data.get('healthy')
            id = data.get('id')

            # 打印获取到的数据
            print('用户名:', username)
            print('学号/工号:', gender)
            print('身份证号:', ids)
            print('部门:', healthy)
            print('id:', id)

            # 创建 PersonProfile 实例并保存数据
            person = HealthInfo.objects.create(
                gender=gender,
                health=healthy,
                personinfo_id=id,
            )
            # 返回成功响应
            return HttpResponse("添加成功")

        except json.JSONDecodeError:
            return JsonResponse({'error': '无法解析JSON数据'}, status=400)

    # 如果请求方法不是POST，返回错误响应
    return HttpResponse("只允许POST请求")