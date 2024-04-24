from functools import wraps
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import  messages
from django.shortcuts import redirect

def login_required(func):
    @wraps(func)
    def inner_func(request, *args, **kwargs):
        if not 'username' in request.session:
            messages.error(request, '请先登录!')
            return HttpResponseRedirect(reverse("login"))
        return func(request, *args, **kwargs)
    return inner_func

def admin_required(func):
    @wraps(func)
    def inner_func(request, *args, **kwargs):
        if request.session.get('role') != '管理员':
            messages.error(request, '没有管理员权限!')
            return redirect(request.META.get('HTTP_REFERER'))
        return func(request, *args, **kwargs)
    return inner_func