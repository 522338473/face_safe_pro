# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: resources.py
@time: 2022/5/18 12:11
"""

from import_export import resources

from apps.device import models as device_models


class DeviceInfoResources(resources.ModelResource):
    """设备导入导出"""

    class Meta:
        model = device_models.DeviceInfo
        fields = [
            "name",
            "channel",
            "ip",
            "geo",
            "address",
            "rtsp_address",
            "device_type",
            "is_access",
        ]

    def export(self, queryset=None, *args, **kwargs):
        """导出触发"""
        return super(DeviceInfoResources, self).export(queryset, *args, **kwargs)

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        """保存触发"""
        return super(DeviceInfoResources, self).save_instance(
            instance, using_transactions, dry_run
        )

    def import_obj(self, obj, data, dry_run, **kwargs):
        """导入触发"""
        return super(DeviceInfoResources, self).import_obj(obj, data, dry_run, **kwargs)
