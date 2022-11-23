from django.db import models
from django.conf import settings
from simplepro.components import fields

from public.models import BaseModel
from utils import constant


class OpticalFiberAlarm(BaseModel):
    """
    光纤报警
    """

    position = fields.CharField(
        max_length=8, null=True, blank=True, verbose_name="报警位置(单位 m)"
    )
    createAt = fields.CharField(
        max_length=32, null=True, blank=True, verbose_name="报警时间"
    )
    geo = fields.AMapField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name="经纬度坐标",
        help_text="点击获取经纬度坐标",
    )
    channel = fields.IntegerField(default=0, verbose_name="通道号")
    devIp = fields.CharField(max_length=32, null=True, blank=True, verbose_name="设备IP")
    alarmType = fields.IntegerField(
        choices=constant.ALARM_TYPE,
        null=True,
        blank=True,
        verbose_name="报警类型(1: 震动 2: 断纤)",
    )

    class Meta:
        verbose_name = "光纤报警"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "".join([self.devIp])

    def alarm_detail(self):
        return "光纤 {position} 米处 {alarm}".format(
            position=self.position, alarm=constant.ALARM_TYPE[self.alarmType - 1][1]
        )


class AlgorithmAlarm(BaseModel):
    """
    算法报警
    """

    device = fields.ForeignKey(
        to="device.DeviceInfo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="报警设备",
    )
    optical = fields.ForeignKey(
        to=OpticalFiberAlarm,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="光纤报警",
    )
    back_path = fields.ImageField(
        drag=True,
        action="/f_upload/snap/",
        null=True,
        blank=True,
        max_length=64,
        verbose_name="背景照",
    )
    take_photo_time = fields.DateTimeField(verbose_name="抓拍时间")

    class Meta:
        verbose_name = "算法报警"
        verbose_name_plural = verbose_name

    def get_back_url(self):
        """背景照路径"""
        if self.back_path:
            return "".join([settings.FAST_DFS_HOST, self.back_path, "?download=0"])
        else:
            return ""


class RollCallHistory(BaseModel):
    """
    点名系统历史快照表
    新增人员名单: 重点人员
    名单人员报警: 重点人员预警
    最近一次报警: 最近一次预警统计
    可筛选记录记录: 历史统计信息[列表，可查看详情]
    5分钟定时任务触发
    """

    start_time = fields.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    end_time = fields.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    personnel_types = fields.CharField(
        max_length=32, null=True, blank=True, verbose_name="名称"
    )
    total_person = fields.IntegerField(default=0, verbose_name="总人数")
    attendance_person = fields.IntegerField(default=0, verbose_name="已出勤人数")
    rate_of_attendance = fields.RateField(default=0.0, verbose_name="出勤率")
    person_list = fields.CharField(
        max_length=512, null=True, blank=True, verbose_name="人员列表"
    )  # 存储id
    person_list_record = fields.CharField(
        max_length=512, null=True, blank=True, verbose_name="人员出勤抓拍"
    )  # 存储id

    class Meta:
        verbose_name = "点名快照"
        verbose_name_plural = verbose_name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.rate_of_attendance == 0.0:
            self.rate_of_attendance = (
                round(self.attendance_person / self.total_person, 2) * 5
            )
        return super(RollCallHistory, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
