# Generated by Django 3.2.13 on 2022-06-09 13:10

from django.db import migrations, models
import django.db.models.deletion
import simplepro.components.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("archives", "0001_initial"),
        ("device", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArchivesLibrary",
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
                        blank=True, max_length=32, null=True, verbose_name="库名"
                    ),
                ),
            ],
            options={
                "verbose_name": "归档库",
                "verbose_name_plural": "归档库",
            },
        ),
        migrations.CreateModel(
            name="ArchivesPersonnel",
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
                        blank=True, max_length=32, null=True, verbose_name="姓名"
                    ),
                ),
                (
                    "gender",
                    simplepro.components.fields.IntegerField(
                        choices=[(1, "男"), (2, "女"), (3, "未知")],
                        default=1,
                        verbose_name="性别",
                    ),
                ),
                (
                    "phone",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="电话号码"
                    ),
                ),
                (
                    "id_card",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="身份证号"
                    ),
                ),
                (
                    "photo",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=128, null=True, verbose_name="照片"
                    ),
                ),
                (
                    "library",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="monitor.archiveslibrary",
                        verbose_name="所属库",
                    ),
                ),
            ],
            options={
                "verbose_name": "归档人员",
                "verbose_name_plural": "归档人员",
            },
        ),
        migrations.CreateModel(
            name="Monitor",
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
                        max_length=32, verbose_name="姓名"
                    ),
                ),
                (
                    "gender",
                    simplepro.components.fields.IntegerField(
                        choices=[(1, "男"), (2, "女"), (3, "未知")],
                        default=1,
                        verbose_name="性别",
                    ),
                ),
                (
                    "types",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "预警人员"), (1, "重点人员")],
                        default=0,
                        verbose_name="人员分类",
                    ),
                ),
                (
                    "photo",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=128, null=True, verbose_name="照片"
                    ),
                ),
                (
                    "area",
                    simplepro.components.fields.SwitchField(
                        default=False, verbose_name="是否禁区"
                    ),
                ),
                (
                    "area_personnel",
                    simplepro.components.fields.IntegerField(
                        blank=True, null=True, verbose_name="禁区关联人员ID"
                    ),
                ),
                (
                    "num_values",
                    simplepro.components.fields.IntegerField(
                        default=0, verbose_name="关联次数"
                    ),
                ),
                (
                    "id_type",
                    simplepro.components.fields.IntegerField(
                        choices=[(1, "身份证"), (2, "护照"), (3, "港澳居民往来内地通行证"), (4, "其他")],
                        default=1,
                        verbose_name="证件类型",
                    ),
                ),
                (
                    "id_name",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="证件名称"
                    ),
                ),
                (
                    "id_number",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="证件号码"
                    ),
                ),
                (
                    "phone",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="电话号码"
                    ),
                ),
                (
                    "source",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "总控平台"), (1, "子平台")],
                        default=1,
                        verbose_name="数据来源",
                    ),
                ),
                (
                    "right_control",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "总控平台"), (1, "子平台"), (2, "总控平台， 子平台")],
                        default=2,
                        verbose_name="预警范围",
                    ),
                ),
            ],
            options={
                "verbose_name": "重点人员",
                "verbose_name_plural": "重点人员",
            },
        ),
        migrations.CreateModel(
            name="VehicleMonitor",
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
                    "plate",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=16, null=True, verbose_name="车牌号"
                    ),
                ),
                (
                    "types",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "普通车辆"), (1, "重点车辆")],
                        default=1,
                        verbose_name="车辆分类",
                    ),
                ),
                (
                    "name",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="车主姓名"
                    ),
                ),
                (
                    "gender",
                    simplepro.components.fields.IntegerField(
                        choices=[(1, "男"), (2, "女"), (3, "未知")],
                        default=1,
                        verbose_name="性别",
                    ),
                ),
                (
                    "id_type",
                    simplepro.components.fields.IntegerField(
                        choices=[(1, "身份证"), (2, "护照"), (3, "港澳居民往来内地通行证"), (4, "其他")],
                        default=1,
                        verbose_name="证件类型",
                    ),
                ),
                (
                    "id_name",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="证件名称"
                    ),
                ),
                (
                    "id_number",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="证件号码"
                    ),
                ),
                (
                    "phone",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=32, null=True, verbose_name="电话号码"
                    ),
                ),
                (
                    "source",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "总控平台"), (1, "子平台")],
                        default=1,
                        verbose_name="数据来源",
                    ),
                ),
                (
                    "right_control",
                    simplepro.components.fields.IntegerField(
                        choices=[(0, "总控平台"), (1, "子平台"), (2, "总控平台， 子平台")],
                        default=2,
                        verbose_name="预警范围",
                    ),
                ),
            ],
            options={
                "verbose_name": "重点车辆",
                "verbose_name_plural": "重点车辆",
                "unique_together": {("plate", "delete_at")},
            },
        ),
        migrations.CreateModel(
            name="VehicleMonitorDiscover",
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
                        default=False, verbose_name="是否已读"
                    ),
                ),
                (
                    "record",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="device.vehicle",
                        verbose_name="抓拍照片",
                    ),
                ),
                (
                    "target",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="monitor.vehiclemonitor",
                        verbose_name="监控目标",
                    ),
                ),
            ],
            options={
                "verbose_name": "车辆监控",
                "verbose_name_plural": "车辆监控",
            },
        ),
        migrations.CreateModel(
            name="RestrictedArea",
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
                        blank=True, max_length=32, null=True, verbose_name="禁区名"
                    ),
                ),
                (
                    "device_list",
                    simplepro.components.fields.ManyToManyField(
                        blank=True, to="device.DeviceInfo", verbose_name="关联设备"
                    ),
                ),
            ],
            options={
                "verbose_name": "门禁管理",
                "verbose_name_plural": "门禁管理",
            },
        ),
        migrations.CreateModel(
            name="PhotoCluster",
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
                    "device_name",
                    simplepro.components.fields.CharField(
                        max_length=50, verbose_name="设备名"
                    ),
                ),
                (
                    "device_address",
                    simplepro.components.fields.AMapField(
                        blank=True, max_length=128, null=True, verbose_name="设备地址"
                    ),
                ),
                (
                    "device_geo",
                    simplepro.components.fields.AMapField(
                        blank=True, max_length=32, null=True, verbose_name="经纬度"
                    ),
                ),
                (
                    "device_ip",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP地址"
                    ),
                ),
                (
                    "device_channel",
                    simplepro.components.fields.IntegerField(
                        default=0, verbose_name="通道号"
                    ),
                ),
                (
                    "device_take_photo_time",
                    simplepro.components.fields.DateTimeField(verbose_name="抓拍时间"),
                ),
                (
                    "device_head_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="大头照"
                    ),
                ),
                (
                    "device_body_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="全身照"
                    ),
                ),
                (
                    "device_back_path",
                    simplepro.components.fields.ImageField(
                        blank=True, max_length=64, null=True, verbose_name="背景照"
                    ),
                ),
                (
                    "device_face_data",
                    models.JSONField(blank=True, null=True, verbose_name="面部属性"),
                ),
                (
                    "device_human_data",
                    models.JSONField(blank=True, null=True, verbose_name="身体属性"),
                ),
                (
                    "similarity",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=12, null=True, verbose_name="相似度"
                    ),
                ),
                (
                    "archives_personnel",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="monitor.archivespersonnel",
                        verbose_name="图片所属人员",
                    ),
                ),
            ],
            options={
                "verbose_name": "图片分类",
                "verbose_name_plural": "图片分类",
            },
        ),
        migrations.CreateModel(
            name="PersonnelType",
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
                        max_length=32, verbose_name="分类名称"
                    ),
                ),
            ],
            options={
                "verbose_name": "人员分类",
                "verbose_name_plural": "人员分类",
                "unique_together": {("name", "delete_at")},
            },
        ),
        migrations.CreateModel(
            name="MonitorDiscover",
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
                    "similarity",
                    simplepro.components.fields.CharField(
                        blank=True, max_length=12, null=True, verbose_name="相似度"
                    ),
                ),
                (
                    "record",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="device.devicephoto",
                        verbose_name="抓拍照片",
                    ),
                ),
                (
                    "target",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="monitor.monitor",
                        verbose_name="监控目标",
                    ),
                ),
            ],
            options={
                "verbose_name": "预警记录",
                "verbose_name_plural": "预警记录",
            },
        ),
        migrations.AddField(
            model_name="monitor",
            name="personnel_types",
            field=simplepro.components.fields.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="monitor.personneltype",
                verbose_name="人员类别",
            ),
        ),
        migrations.CreateModel(
            name="AreaMonitorPersonnel",
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
                    "area",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="monitor.restrictedarea",
                        verbose_name="禁区",
                    ),
                ),
                (
                    "personnel",
                    simplepro.components.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="archives.personnel",
                        verbose_name="人员",
                    ),
                ),
            ],
            options={
                "verbose_name": "门禁人员",
                "verbose_name_plural": "门禁人员",
                "unique_together": {("personnel", "area", "delete_at")},
            },
        ),
    ]
