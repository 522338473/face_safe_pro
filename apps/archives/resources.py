# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: resources.py
@time: 2022/5/18 12:11
"""

from import_export import resources

from apps.archives import models as archives_models


class PersonnelResources(resources.ModelResource):
    """人员档案导入导出"""

    class Meta:
        model = archives_models.Personnel

    def export(self, queryset=None, *args, **kwargs):
        """导出触发"""
        return super(PersonnelResources, self).export(queryset, *args, **kwargs)

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        """保存触发"""
        return super(PersonnelResources, self).save_instance(
            instance, using_transactions, dry_run
        )

    def import_obj(self, obj, data, dry_run, **kwargs):
        """导入触发"""
        return super(PersonnelResources, self).import_obj(obj, data, dry_run, **kwargs)
