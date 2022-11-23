# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: resources.py
@time: 2022/5/18 12:11
"""

from import_export import resources


from monitor import models as monitor_models


class MonitorResources(resources.ModelResource):
    """重点人员导入导出"""

    class Meta:
        model = monitor_models.Monitor
        fields = [
            "personnel_types",
            "name",
            "gender",
            "types",
            "photo",
            "id_name",
            "id_number",
            "phone",
            "",
        ]

    def export(self, queryset=None, *args, **kwargs):
        """导出触发"""
        return super(MonitorResources, self).export(queryset, *args, **kwargs)

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        """保存触发"""
        return super(MonitorResources, self).save_instance(
            instance, using_transactions, dry_run
        )

    def import_obj(self, obj, data, dry_run, **kwargs):
        """导入触发"""
        return super(MonitorResources, self).import_obj(obj, data, dry_run, **kwargs)


class ArchivesPersonnelResources(resources.ModelResource):
    """关注人员导入导出"""

    class Meta:
        model = monitor_models.ArchivesPersonnel
        fields = ["library", "name", "gender", "phone", "id_card", "photo"]

    def export(self, queryset=None, *args, **kwargs):
        """导出触发"""
        return super(ArchivesPersonnelResources, self).export(queryset, *args, **kwargs)

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        """保存触发"""
        return super(ArchivesPersonnelResources, self).save_instance(
            instance, using_transactions, dry_run
        )

    def import_obj(self, obj, data, dry_run, **kwargs):
        """导入触发"""
        return super(ArchivesPersonnelResources, self).import_obj(
            obj, data, dry_run, **kwargs
        )


class AreaMonitorPersonnelResources(resources.ModelResource):
    """门禁人员导入导出"""

    class Meta:
        model = monitor_models.AreaMonitorPersonnel
        fields = ["personnel", "area"]

    def export(self, queryset=None, *args, **kwargs):
        """导出触发"""
        return super(AreaMonitorPersonnelResources, self).export(
            queryset, *args, **kwargs
        )

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        """保存触发"""
        return super(AreaMonitorPersonnelResources, self).save_instance(
            instance, using_transactions, dry_run
        )

    def import_obj(self, obj, data, dry_run, **kwargs):
        """导入触发"""
        return super(AreaMonitorPersonnelResources, self).import_obj(
            obj, data, dry_run, **kwargs
        )


class VehicleMonitorResources(resources.ModelResource):
    """重点车辆导入导出"""

    class Meta:
        model = monitor_models.VehicleMonitor
        fields = ["plate", "name", "gender", "id_name", "id_number", "phone"]

    def export(self, queryset=None, *args, **kwargs):
        """导出触发"""
        return super(VehicleMonitorResources, self).export(queryset, *args, **kwargs)

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        """保存触发"""
        return super(VehicleMonitorResources, self).save_instance(
            instance, using_transactions, dry_run
        )

    def import_obj(self, obj, data, dry_run, **kwargs):
        """导入触发"""
        return super(VehicleMonitorResources, self).import_obj(
            obj, data, dry_run, **kwargs
        )
