from datetime import datetime

from django.db import models
from django.conf import settings
from simplepro.components import fields

from apps.public.models import BaseModel
from apps.utils import constant


class PersonnelType(BaseModel):
    """
    重点人员分类表
    """

    name = fields.CharField(max_length=32, null=False, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='分类名称', placeholder='请输入分类名称')

    class Meta:
        verbose_name = '人员分类'
        verbose_name_plural = verbose_name
        unique_together = ['name', 'delete_at']

    def __str__(self):
        return self.name


class Monitor(BaseModel):
    """
    重点人员表
    """

    personnel_types = fields.ForeignKey(to='PersonnelType', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='人员类别')

    name = fields.CharField(null=False, blank=False, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='姓名', placeholder='请输入重点人员姓名')
    gender = fields.IntegerField(choices=constant.GENDER, default=1, verbose_name='性别')
    types = fields.IntegerField(choices=constant.PERSON_TYPES, default=0, verbose_name='人员分类')
    photo = fields.ImageField(drag=True, null=True, blank=True, max_length=128, verbose_name='照片')
    area = fields.SwitchField(default=False, verbose_name='是否禁区')
    area_personnel = fields.IntegerField(null=True, blank=True, verbose_name='禁区关联人员ID')
    num_values = fields.IntegerField(default=0, verbose_name='关联次数')
    id_type = fields.IntegerField(choices=constant.TYPES, default=1, verbose_name='证件类型')
    id_name = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='证件名称', placeholder='请输入证件名称')
    id_number = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='证件号码', placeholder='请输入证件号码')
    phone = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='电话号码', placeholder='请输入电话号码')
    source = fields.IntegerField(choices=constant.SOURCE, default=1, verbose_name='数据来源')
    right_control = fields.IntegerField(choices=constant.CONTROL, default=2, verbose_name='预警范围')

    class Meta:
        verbose_name = '重点人员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def set_delete(self):
        """删除预警人员的时候删除预警信息"""
        self.monitordiscover_set.get_queryset().update(delete_at=datetime.now())
        self.delete_at = datetime.now()
        self.save()

    def get_head_url(self):
        return ''.join([settings.FAST_DFS_HOST, self.photo, '?download=0'])


class MonitorDiscover(BaseModel):
    """
    重点人员报警记录表
    """

    target = fields.ForeignKey(to='Monitor', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='监控目标')
    record = fields.ForeignKey(to='device.DevicePhoto', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='抓拍照片')

    checked = fields.SwitchField(default=False, verbose_name='已读未读')
    similarity = fields.CharField(null=True, blank=True, max_length=12, verbose_name='相似度')

    class Meta:
        verbose_name = '预警记录'
        verbose_name_plural = verbose_name


class VehicleMonitor(BaseModel):
    """
    重点车辆管理表
    """

    plate = fields.CharField(null=True, blank=True, max_length=16, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='车牌号', placeholder='请输入车牌号')
    types = fields.IntegerField(choices=constant.VEHICLE_TYPES, default=1, verbose_name='车辆分类')
    name = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='车主姓名', placeholder='请输入车主姓名')
    gender = fields.IntegerField(choices=constant.GENDER, default=1, verbose_name='性别')
    id_type = fields.IntegerField(choices=constant.TYPES, default=1, verbose_name='证件类型')
    id_name = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='证件名称', placeholder='请输入证件名称')
    id_number = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='证件号码', placeholder='请输入证件号码')
    phone = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='电话号码', placeholder='请输入电话号码')
    source = fields.IntegerField(choices=constant.SOURCE, default=1, verbose_name='数据来源')
    right_control = fields.IntegerField(choices=constant.CONTROL, default=2, verbose_name='预警范围')

    class Meta:
        verbose_name = '重点车辆'
        verbose_name_plural = verbose_name
        unique_together = ['plate', 'delete_at']

    def __str__(self):
        return self.plate

    def set_delete(self):
        """删除预警车辆的时候删除预警信息"""
        self.vehiclemonitordiscover_set.get_queryset().update(delete_at=datetime.now())
        self.delete_at = datetime.now()
        self.save()

    def get_id_type(self):
        if self.id_type == 4:
            return self.id_name
        else:
            return constant.TYPES[self.id_type - 1][1]

    def get_source(self):
        return constant.SOURCE[self.source][1]

    def get_right_control(self):
        return constant.CONTROL[self.right_control][1]


class VehicleMonitorDiscover(BaseModel):
    """
    车辆监控发现记录表
    """

    target = fields.ForeignKey(to='VehicleMonitor', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='监控目标')
    record = fields.ForeignKey(to='device.Vehicle', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='抓拍照片')

    checked = fields.SwitchField(default=False, verbose_name='是否已读')

    class Meta:
        verbose_name = '车辆监控'
        verbose_name_plural = verbose_name


# TODO: personnel_list 该字段后期删除，区域人员以: AreaMonitorPersonnel为准
class RestrictedArea(BaseModel):
    """
    区域管理表
    """

    name = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='禁区名', placeholder='请输入禁区名称')

    device_list = fields.ManyToManyField(to='device.DeviceInfo', blank=True, verbose_name='关联设备')
    personnel_list = fields.ManyToManyField(to='archives.Personnel', blank=True, verbose_name='关联人员')

    class Meta:
        verbose_name = '门禁管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# TODO: 该表与上表有冲突。后期讨论优化
class AreaMonitorPersonnel(BaseModel):
    """
    区域监测人员表
    """

    personnel = fields.ForeignKey(to='archives.Personnel', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='人员')
    area = fields.ForeignKey(to='RestrictedArea', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='禁区')

    class Meta:
        verbose_name = '门禁人员'
        verbose_name_plural = verbose_name


# TODO: 跟门禁通行冗余
class AreaSnapRecord(BaseModel):
    """
    区域抓拍记录表
    """

    personnel = fields.ForeignKey(to='AreaMonitorPersonnel', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="区域人员")
    record = fields.ForeignKey(to='device.DevicePhoto', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="抓拍目标")

    checked = fields.SwitchField(default=False, verbose_name='已读未读')
    similarity = fields.CharField(null=True, blank=True, max_length=12, verbose_name='相似度')

    class Meta:
        verbose_name = '门禁抓拍'
        verbose_name_plural = verbose_name


class ArchivesLibrary(BaseModel):
    """
    关注人员库--归档库
    """

    name = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='库名')

    class Meta:
        verbose_name = '归档库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_personnel_count(self):
        """获取当前库下的所有人员总数"""
        return self.archivespersonnel_set.filter(delete_at__isnull=True).count()

    def get_personnel(self):
        """获取当前库下的所有人员"""
        return self.archivespersonnel_set.values()

    def set_delete(self):
        self.archivespersonnel_set.get_queryset().update(delete_at=datetime.now())
        self.delete_at = datetime.now()
        self.save()


class ArchivesPersonnel(BaseModel):
    """
    关注人员---归档人员
    """

    library = fields.ForeignKey(to='ArchivesLibrary', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属库')
    name = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='姓名', placeholder='请输入人员姓名')
    gender = fields.IntegerField(choices=constant.GENDER, default=1, verbose_name='性别')
    phone = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='电话号码', placeholder='请输入电话号码')
    id_card = fields.CharField(null=True, blank=True, max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='身份证号', placeholder='请输入身份证号码')
    photo = fields.ImageField(drag=True, null=True, blank=True, max_length=128, verbose_name='照片')

    class Meta:
        verbose_name = '归档人员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '_'.join([self.library.name, self.name]) if self.library else '_'.join([self.name])

    def get_head_url(self):
        return ''.join([settings.FAST_DFS_HOST, self.photo, '?download=0'])


class PhotoCluster(BaseModel):
    """
    抓拍图片分类
    """

    archives_personnel = fields.ForeignKey(to='ArchivesPersonnel', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='图片所属人员')

    device_name = fields.CharField(null=False, blank=False, max_length=50, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='设备名')
    device_address = fields.AMapField(max_length=128, null=True, blank=True, pick_type='address', verbose_name='设备地址')
    device_geo = fields.AMapField(max_length=32, null=True, blank=True, verbose_name='经纬度')
    device_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    device_channel = fields.IntegerField(default=0, verbose_name='通道号')
    device_take_photo_time = fields.DateTimeField(verbose_name='抓拍时间')
    device_head_path = fields.ImageField(drag=True, null=True, blank=True, max_length=64, verbose_name='大头照')
    device_body_path = fields.ImageField(drag=True, null=True, blank=True, max_length=64, verbose_name='全身照')
    device_back_path = fields.ImageField(drag=True, null=True, blank=True, max_length=64, verbose_name='背景照')
    device_face_data = models.JSONField(null=True, blank=True, verbose_name='面部属性')
    device_human_data = models.JSONField(null=True, blank=True, verbose_name='身体属性')
    similarity = fields.CharField(null=True, blank=True, max_length=12, verbose_name='相似度')

    class Meta:
        verbose_name = '图片分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.archives_personnel.name if self.archives_personnel else ''

    def get_head_url(self):
        return ''.join([settings.FAST_DFS_HOST, self.device_head_path, '?download=0'])

    def get_body_url(self):
        return ''.join([settings.FAST_DFS_HOST, self.device_body_path, '?download=0'])

    def get_back_url(self):
        return ''.join([settings.FAST_DFS_HOST, self.device_back_path, '?download=0'])
