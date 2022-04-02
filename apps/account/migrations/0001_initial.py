# Generated by Django 3.2.12 on 2022-04-02 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simplepro.components.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', simplepro.components.fields.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', simplepro.components.fields.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('delete_at', simplepro.components.fields.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('create_by', simplepro.components.fields.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('detail', simplepro.components.fields.CharField(blank=True, max_length=200, null=True, verbose_name='备注信息')),
                ('mobile', simplepro.components.fields.IntegerField(blank=True, null=True, verbose_name='手机号')),
                ('user', simplepro.components.fields.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='用户默认配置')),
            ],
            options={
                'verbose_name': '用户信息扩展字段',
                'verbose_name_plural': '用户信息扩展字段',
            },
        ),
    ]
