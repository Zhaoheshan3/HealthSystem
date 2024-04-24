# Generated by Django 4.2.9 on 2024-01-31 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('num', models.CharField(max_length=10, verbose_name='工号')),
                ('id_num', models.CharField(max_length=30, unique=True, verbose_name='身份证号')),
                ('depart', models.CharField(max_length=30, verbose_name='部门')),
                ('role', models.CharField(max_length=20, verbose_name='身份')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('role', models.CharField(max_length=20, verbose_name='角色')),
            ],
        ),
        migrations.CreateModel(
            name='HealthInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10, verbose_name='性别')),
                ('health', models.CharField(max_length=20, verbose_name='症状')),
                ('comment', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('personinfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='healthapp.personprofile')),
            ],
        ),
    ]
