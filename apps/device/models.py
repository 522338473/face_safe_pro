from datetime import datetime

from django.db import models
from django.conf import settings
from simplepro.components import fields

from apps.public.models import BaseModel
from apps.utils import constant


class DeviceInfo(BaseModel):
    """
    设备信息表
    """
    name = fields.CharField(null=False, blank=False, max_length=50, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='设备名', placeholder='请输入设备名称')
    channel = fields.IntegerField(default=0, verbose_name='通道号')
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    status = fields.IntegerField(choices=constant.STATUS_CHOICE, default=1, verbose_name='设备状态')
    geo = fields.AMapField(max_length=32, null=True, blank=True, verbose_name='经纬度坐标', help_text='点击获取经纬度坐标')
    address = fields.AMapField(max_length=128, null=True, blank=True, pick_type='address', verbose_name='设备地址', help_text='点击地图获取地址')
    rtsp_address = fields.CharField(max_length=128, null=True, blank=True, show_word_limit=True, suffix_icon='el-icon-coffee', verbose_name='rtsp地址', placeholder='请输入RTSP地址')
    last_login = fields.DateTimeField(blank=True, null=True, verbose_name='最后一次连接时间')
    last_logout = fields.DateTimeField(blank=True, null=True, verbose_name='最后一次下线时间')
    is_access = fields.IntegerField(choices=constant.IS_ACCESS, default=0, verbose_name='是否门禁设备')
    device_type = fields.IntegerField(choices=constant.DEVICE_TYPE, default=0, verbose_name='设备类型')
    snap_count = fields.IntegerField(default=0, verbose_name='总抓拍')
    monitor_count = fields.IntegerField(default=0, verbose_name='总预警')

    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name
        unique_together = ['name', 'ip', 'delete_at']

    def __str__(self):
        return self.name

    def device_login(self):
        self.status = 1
        self.last_login = datetime.now()
        return self.save()

    def device_logout(self):
        self.status = 0
        self.last_logout = datetime.now()
        return self.save()


class DevicePhoto(BaseModel):
    """
    抓拍记录表
    """

    device = fields.ForeignKey(to='DeviceInfo', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属设备')

    take_photo_time = fields.DateTimeField(verbose_name='抓拍时间')
    head_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='大头照')
    body_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='全身照')
    back_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='背景照')
    face_data = models.JSONField(null=True, blank=True, verbose_name='面部属性')
    human_data = models.JSONField(null=True, blank=True, verbose_name='身体属性')
    address = fields.AMapField(max_length=128, null=True, blank=True, pick_type='address', verbose_name='抓拍地址')
    geo = fields.AMapField(max_length=32, null=True, blank=True, verbose_name='经纬度坐标')

    class Meta:
        verbose_name = '抓拍图像'
        verbose_name_plural = verbose_name
        ordering = ['-take_photo_time']

    def get_head_url(self):
        """人脸路径"""
        if self.head_path:
            return ''.join([settings.FAST_DFS_HOST, self.head_path, '?download=0'])
        else:
            return ''

    def get_body_url(self):
        """全身照路径"""
        if self.body_path:
            return ''.join([settings.FAST_DFS_HOST, self.body_path, '?download=0'])
        else:
            return ''

    def get_back_url(self):
        """背景照路径"""
        if self.back_path:
            return ''.join([settings.FAST_DFS_HOST, self.back_path, '?download=0'])
        else:
            return ''

    def __str__(self):
        return self.head_path


class Vehicle(BaseModel):
    """
    车辆管理表
    """

    device = fields.ForeignKey(to='DeviceInfo', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='设备名')

    take_photo_time = fields.DateTimeField(verbose_name='抓拍时间')
    types = fields.CharField(null=True, blank=True, max_length=8, verbose_name='车辆类型')
    color = fields.CharField(null=True, blank=True, max_length=8, verbose_name='车辆颜色')
    plate = fields.CharField(null=True, blank=True, max_length=8, verbose_name='车牌号')
    plate_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='车牌照')
    vehicle_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='车辆特写照')
    panorama_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='车辆全景照')
    address = fields.AMapField(max_length=128, null=True, blank=True, pick_type='address', verbose_name='抓拍地址')
    geo = fields.AMapField(max_length=32, null=True, blank=True, verbose_name='经纬度坐标')

    class Meta:
        verbose_name = '车辆信息'
        verbose_name_plural = verbose_name
        ordering = ['-take_photo_time']

    def get_plate_url(self):
        """车牌照"""
        if self.plate_path:
            return ''.join([settings.FAST_DFS_HOST, self.plate_path, '?download=0'])
        else:
            return ''

    def get_vehicle_url(self):
        """车辆照"""
        if self.vehicle_path:
            return ''.join([settings.FAST_DFS_HOST, self.vehicle_path, '?download=0'])
        else:
            return ''

    def get_panorama_url(self):
        """车辆全景照"""
        if self.panorama_path:
            return ''.join([settings.FAST_DFS_HOST, self.panorama_path, '?download=0'])
        else:
            return ''

    def __str__(self):
        return self.plate_path


class Motor(BaseModel):
    """
    非机动车管理表
    """

    device = fields.ForeignKey(to='DeviceInfo', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='设备名')

    take_photo_time = fields.DateTimeField(verbose_name='抓拍时间')
    types = fields.CharField(null=True, blank=True, max_length=8, verbose_name='车辆类型')
    motor_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='车辆特写照')
    panorama_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='车辆全景照')
    address = fields.AMapField(max_length=128, null=True, blank=True, pick_type='address', verbose_name='抓拍地址')
    geo = fields.AMapField(max_length=32, null=True, blank=True, verbose_name='经纬度经纬度')

    class Meta:
        verbose_name = "非机动车信息"
        verbose_name_plural = verbose_name
        ordering = ['-take_photo_time']

    def get_motor_url(self):
        """非机动车特写照"""
        if self.motor_path:
            return ''.join([settings.FAST_DFS_HOST, self.motor_path, '?download=0'])
        else:
            return ''

    def get_panorama_url(self):
        """非机动车全景照"""
        if self.panorama_path:
            return ''.join([settings.FAST_DFS_HOST, self.panorama_path, '?download=0'])
        else:
            return ''


class DeviceOffLine(BaseModel):
    """
    设备离线记录表
    """

    device = fields.ForeignKey(to='DeviceInfo', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='设备名')

    checked = fields.SwitchField(default=False, verbose_name='已读未读')
    alarm_type = fields.CharField(max_length=32, show_word_limit=True, suffix_icon='el-icon-coffee', default='设备离线', verbose_name='报警类型')
    photo_path = fields.ImageField(drag=True, action='/f_upload/snap/', null=True, blank=True, max_length=64, verbose_name='图片路径')

    class Meta:
        verbose_name = "设备报警"
        verbose_name_plural = verbose_name

    def get_photo_url(self):
        """报警图片链接"""
        if self.photo_path:
            return ''.join([settings.FAST_DFS_HOST, self.photo_path, '?download=0'])
        else:
            return ''
