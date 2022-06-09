# Generated by Django 3.2.13 on 2022-06-09 13:10

from django.db import migrations, models
import django.db.models.deletion
import simplepro.components.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DeviceInfo",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "create_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "update_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now=True, verbose_name="更新时间"
                    ),
                ),
                (
                    "delete_at",
                    simplepro.components.fields.DateTimeField(
                        blank=True, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "create_by",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="创建人"
                    ),
                ),
                (
                    "detail",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=200, null=True, verbose_name="备注信息"
                    ),
                ),
                (
                    "name",
                    simplepro.components.fields.CharField(
                        max_length=50, verbose_name="设备名"
                    ),
                ),
                (
                    "channel",
                    simplepro.components.fields.IntegerField(
                        default=0, verbose_name="通道号"
                    ),
                ),
                (
                    "ip",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP地址"
                    ),
                ),
                (
                    "status",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "离线"), (1, "在线")], default=1, verbose_name="设备状态"
                    ),
                ),
                (
                    "geo",
                    simplepro.components.fields.AMapField(
                        blank=True,
                        help_text="点击获取经纬度坐标",
                        max_length=32,
                        null=True,
                        verbose_name="经纬度坐标",
                    ),
                ),
                (
                    "address",
                    simplepro.components.fields.AMapField(
                        blank=True,
                        help_text="点击地图获取地址",
                        max_length=128,
                        null=True,
                        verbose_name="设备地址",
                    ),
                ),
                (
                    "rtsp_address",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=128, null=True, verbose_name="rtsp地址"
                    ),
                ),
                (
                    "last_login",
                    simplepro.components.fields.DateTimeField(
                        blank=True, null=True, verbose_name="最后一次连接时间"
                    ),
                ),
                (
                    "last_logout",
                    simplepro.components.fields.DateTimeField(
                        blank=True, null=True, verbose_name="最后一次下线时间"
                    ),
                ),
                (
                    "is_access",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "否"), (1, "是")], default=0, verbose_name="是否门禁设备"
                    ),
                ),
                (
                    "device_type",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "普通相机"), (1, "人脸相机"), (2, "门禁设备"), (3, "无感通行")],
                        default=0,
                        verbose_name="设备类型",
                    ),
                ),
                (
                    "snap_count",
                    simplepro.components.fields.IntegerField(
                        default=0, verbose_name="总抓拍"
                    ),
                ),
                (
                    "monitor_count",
                    simplepro.components.fields.IntegerField(
                        default=0, verbose_name="总预警"
                    ),
                ),
            ],
            options={
                "verbose_name": "设备信息",
                "verbose_name_plural": "设备信息",
                "unique_together": {("name", "ip", "delete_at")},
            },
        ),
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "create_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "update_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now=True, verbose_name="更新时间"
                    ),
                ),
                (
                    "delete_at",
                    simplepro.components.fields.DateTimeField(
                        blank=True, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "create_by",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="创建人"
                    ),
                ),
                (
                    "detail",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=200, null=True, verbose_name="备注信息"
                    ),
                ),
                (
                    "take_photo_time",
                    simplepro.components.fields.DateTimeField(verbose_name="抓拍时间"),
                ),
                (
                    "types",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=8, null=True, verbose_name="车辆类型"
                    ),
                ),
                (
                    "color",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=8, null=True, verbose_name="车辆颜色"
                    ),
                ),
                (
                    "plate",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=8, null=True, verbose_name="车牌号"
                    ),
                ),
                (
                    "plate_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="车牌照"
                    ),
                ),
                (
                    "vehicle_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="车辆特写照"
                    ),
                ),
                (
                    "panorama_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="车辆全景照"
                    ),
                ),
                (
                    "address",
                    simplepro.components.fields.AMapField(
                        blank=True, max_length=128, null=True, verbose_name="抓拍地址"
                    ),
                ),
                (
                    "geo",
                    simplepro.components.fields.AMapField(
                        blank=True, max_length=32, null=True, verbose_name="经纬度坐标"
                    ),
                ),
                (
                    "device",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="device.deviceinfo",
                        verbose_name="设备名",
                    ),
                ),
            ],
            options={
                "verbose_name": "车辆信息",
                "verbose_name_plural": "车辆信息",
                "ordering": ["-take_photo_time"],
            },
        ),
        migrations.CreateModel(
            name="Motor",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "create_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "update_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now=True, verbose_name="更新时间"
                    ),
                ),
                (
                    "delete_at",
                    simplepro.components.fields.DateTimeField(
                        blank=True, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "create_by",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="创建人"
                    ),
                ),
                (
                    "detail",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=200, null=True, verbose_name="备注信息"
                    ),
                ),
                (
                    "take_photo_time",
                    simplepro.components.fields.DateTimeField(verbose_name="抓拍时间"),
                ),
                (
                    "types",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=8, null=True, verbose_name="车辆类型"
                    ),
                ),
                (
                    "motor_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="车辆特写照"
                    ),
                ),
                (
                    "panorama_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="车辆全景照"
                    ),
                ),
                (
                    "address",
                    simplepro.components.fields.AMapField(
                        blank=True, max_length=128, null=True, verbose_name="抓拍地址"
                    ),
                ),
                (
                    "geo",
                    simplepro.components.fields.AMapField(
                        blank=True, max_length=32, null=True, verbose_name="经纬度经纬度"
                    ),
                ),
                (
                    "device",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="device.deviceinfo",
                        verbose_name="设备名",
                    ),
                ),
            ],
            options={
                "verbose_name": "非机动车信息",
                "verbose_name_plural": "非机动车信息",
                "ordering": ["-take_photo_time"],
            },
        ),
        migrations.CreateModel(
            name="DevicePhoto",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "create_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "update_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now=True, verbose_name="更新时间"
                    ),
                ),
                (
                    "delete_at",
                    simplepro.components.fields.DateTimeField(
                        blank=True, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "create_by",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="创建人"
                    ),
                ),
                (
                    "detail",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=200, null=True, verbose_name="备注信息"
                    ),
                ),
                (
                    "take_photo_time",
                    simplepro.components.fields.DateTimeField(verbose_name="抓拍时间"),
                ),
                (
                    "head_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="大头照"
                    ),
                ),
                (
                    "body_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="全身照"
                    ),
                ),
                (
                    "back_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="背景照"
                    ),
                ),
                (
                    "face_data",
                    models.JSONField(blank=True, null=True, verbose_name="面部属性"),
                ),
                (
                    "human_data",
                    models.JSONField(blank=True, null=True, verbose_name="身体属性"),
                ),
                (
                    "address",
                    simplepro.components.fields.AMapField(
                        blank=True, max_length=128, null=True, verbose_name="抓拍地址"
                    ),
                ),
                (
                    "geo",
                    simplepro.components.fields.AMapField(
                        blank=True, max_length=32, null=True, verbose_name="经纬度坐标"
                    ),
                ),
                (
                    "device",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="device.deviceinfo",
                        verbose_name="所属设备",
                    ),
                ),
            ],
            options={
                "verbose_name": "抓拍图像",
                "verbose_name_plural": "抓拍图像",
                "ordering": ["-take_photo_time"],
            },
        ),
        migrations.CreateModel(
            name="DeviceOffLine",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "create_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "update_at",
                    simplepro.components.fields.DateTimeField(
                        auto_now=True, verbose_name="更新时间"
                    ),
                ),
                (
                    "delete_at",
                    simplepro.components.fields.DateTimeField(
                        blank=True, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "create_by",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="创建人"
                    ),
                ),
                (
                    "detail",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=200, null=True, verbose_name="备注信息"
                    ),
                ),
                (
                    "checked",
                    simplepro.components.fields.SwitchField(
                        default=False, verbose_name="已读未读"
                    ),
                ),
                (
                    "alarm_type",
                    simplepro.components.fields.CharField(
                        default="设备离线", max_length=32, verbose_name="报警类型"
                    ),
                ),
                (
                    "photo_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="图片路径"
                    ),
                ),
                (
                    "device",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="device.deviceinfo",
                        verbose_name="设备名",
                    ),
                ),
            ],
            options={
                "verbose_name": "设备报警",
                "verbose_name_plural": "设备报警",
            },
        ),
    ]
