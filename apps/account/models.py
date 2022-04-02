from django.db import models
from django.contrib.auth.models import User

from simplepro.components import fields

from apps.public.models import BaseModel


class UserExtra(BaseModel):
    """
    用户信息扩展
    """

    user = fields.OneToOneField(to=User, null=True, blank=True, related_name='user', on_delete=models.SET_NULL, verbose_name='用户默认配置')
    mobile = fields.IntegerField(null=True, blank=True, verbose_name='手机号')

    class Meta:
        verbose_name = '用户信息扩展字段'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
