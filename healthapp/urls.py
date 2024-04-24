from django.urls import path
from . import views

from .views import (PersonInfoListView, UserInfoListView, HealthInfoListView)
from .utils import login_required,admin_required

app_name = "health"

urlpatterns = [
    path('', views.index, name='index'),
    path('userinfo', admin_required(UserInfoListView.as_view()), name='userinfo'),
    path('adduser', views.adduser, name='adduser'),
    path('edituser/<int:id>', views.edituser, name='edituser'),
    path('deluser/<int:id>', views.deluser, name='deluser'),
    path('personinfo', login_required(PersonInfoListView.as_view()), name='personinfo'),
    path('upload_personinfo', views.upload_personinfo_xls, name='upload_personinfo'),
    path('delperson/<int:id>', views.delperson, name='delperson'),
    path('healthinfo', login_required(HealthInfoListView.as_view()), name='healthinfo'),
    path('upload_healthinfo', views.upload_healthinfo_xls, name='upload_healthinfo'),
    path('edithealth/<int:id>', views.edithealth, name='edithealth'),
    path('delhealth/<int:id>', views.delhealth, name='delhealth'),

    # path('login', views.login, name='login'),
    # path('logout', views.logout, name='logout'),
    # path('profile', views.profile, name='profile'),
]