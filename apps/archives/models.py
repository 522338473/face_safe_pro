from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from simplepro.components import fields

from apps.public.models import BaseModel
from apps.utils import constant


class ArchivesGroup(BaseModel):
    """
    档案分组表
    """

    name = fields.CharField(max_length=32, null=False, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='库名', placeholder='请输入档案分组名称')

    class Meta:
        verbose_name = '档案库'
        verbose_name_plural = verbose_name
        unique_together = ['name', 'delete_at']

    def __str__(self):
        return self.name


class Personnel(BaseModel):
    """
    人员表
    """

    archives_group = fields.ForeignKey(to='ArchivesGroup', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="档案分组名称")

    name = fields.CharField(null=False, blank=False, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='姓名', placeholder='请输入人员名称')
    gender = fields.IntegerField(choices=constant.GENDER, default=1, verbose_name='性别')
    phone = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='手机号', placeholder='请输入手机号')
    photo = fields.ImageField(drag=True, action='/f_upload/archives/', null=True, blank=True, max_length=128, verbose_name='照片')
    id_card = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='身份证号', placeholder='请输入身份证号码')
    household_register = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='户籍', placeholder='请输入户籍所在地')
    date_of_birth = fields.CharField(null=True, blank=True, max_length=12, suffix_icon='el-icon-coffee', verbose_name='出生年月', placeholder='请输入出生年月: 1900-01-01')
    nation = fields.CharField(null=True, blank=True, max_length=32, suffix_icon='el-icon-coffee', verbose_name='民族', placeholder='请输入民族')
    nationality = fields.CharField(null=True, blank=True, max_length=32, suffix_icon='el-icon-coffee', verbose_name='国籍', placeholder='请输入国籍')
    id_type = fields.IntegerField(choices=constant.TYPES, default=1, verbose_name='证件类型')
    id_name = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='证件名称', placeholder='请输入证件名称')
    source = fields.IntegerField(choices=constant.SOURCE, default=1, verbose_name='数据来源')
    right_control = fields.IntegerField(choices=constant.CONTROL, default=2, verbose_name='预警范围')
    address = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name="住址", placeholder='请输入地址')
    is_access = fields.IntegerField(default=0, choices=constant.IS_ACCESS, verbose_name='是否门禁人员')
    # TODO: 该字段扩展。后期决定存留
    device_list = fields.ManyToManyField(to='device.DeviceInfo', blank=True, verbose_name='人员所属门禁')

    class Meta:
        verbose_name = '档案人员库'
        verbose_name_plural = verbose_name
        unique_together = ['name', 'phone', 'delete_at']

    def __str__(self):
        return self.name

    def get_head_url(self):
        return ''.join([settings.FAST_DFS_HOST, self.photo, '?download=0'])

    def head_image(self):
        return mark_safe('<img src="%s" width=30px;>' % self.photo)

    head_image.short_description = 'Model头像'


class AccessDiscover(BaseModel):
    """
    门禁通行记录表
    """

    target = fields.ForeignKey(to='Personnel', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='门禁人员档案')
    record = fields.ForeignKey(to='device.DevicePhoto', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='通行抓拍')

    checked = fields.SwitchField(default=False, verbose_name='已读未读')
    similarity = fields.CharField(null=True, blank=True, max_length=12, verbose_name='相似度')

    class Meta:
        verbose_name = '门禁通行记录'
        verbose_name_plural = verbose_name
