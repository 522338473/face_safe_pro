from django.urls import reverse
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simplepro.dialog import ModalDialog, MultipleCellDialog

from apps.monitor import models as monitor_models
from apps.public.admin import PublicModelAdmin
from apps.public.resources import MonitorResources, ArchivesPersonnelResources


# Register your models here.


@admin.register(monitor_models.PersonnelType)
class PersonnelTypeAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'detail']
    search_fields = ['name']


@admin.register(monitor_models.Monitor)
class MonitorAdmin(PublicModelAdmin, ImportExportModelAdmin):
    list_display = ['id', 'name', 'personnel_types', 'gender', 'phone', 'photo', 'operation']
    list_filter = ['personnel_types', 'create_at']
    exclude = ['num_values', 'area_personnel']
    search_fields = ['name']
    resource_class = MonitorResources
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'name': {
            'width': '120px'
        },
        'personnel_types': {
            'width': '160px'
        },
        'gender': {
            'width': '80px'
        },
        'phone': {
            'width': '120px'
        },
        'operation': {
            'width': '120px'
        }
    }

    def operation(self, model):
        record = ModalDialog(
            cell='<el-link type="primary">抓拍记录</el-link>',
            title='抓拍记录',
            url=reverse('device:photo_search') + "?id=%s" % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        return MultipleCellDialog([record])

    operation.short_description = '操作'


@admin.register(monitor_models.MonitorDiscover)
class MonitorDiscoverAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'target', 'record', 'checked', 'similarity', 'operation']
    list_filter = ['record__take_photo_time', 'target']
    search_fields = ['target__name']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'target': {
            'width': '120px'
        },
        'checked': {
            'width': '120px'
        },
        'similarity': {
            'width': '100px'
        },
        'operation': {
            'width': '300px'
        }
    }

    def operation(self, model):
        detail = ModalDialog(
            cell='<el-link type="primary">详情</el-link>',
            title='当前数据详情',
            url=reverse('device:photo_detail') + "?id=%s" % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        back = ModalDialog(
            cell='<el-link type="primary">回放视频</el-link>',
            title='回放视频',
            url=reverse('device:video_playback') + '?id=%s' % model.id,
            height='435px',
            width='800px',
            show_cancel=True
        )
        return MultipleCellDialog([detail, back])

    operation.short_description = '操作'


@admin.register(monitor_models.VehicleMonitor)
class VehicleMonitorAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'plate', 'name', 'gender', 'phone', 'detail', 'operation']
    search_fields = ['plate', 'name', 'phone']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'plate': {
            'width': '120px'
        },
        'name': {
            'width': '120px'
        },
        'gender': {
            'width': '80px'
        },
        'phone': {
            'width': '120px'
        },
    }

    def operation(self, model):
        record = ModalDialog(
            cell='<el-link type="primary">抓拍记录</el-link>',
            title='重点车辆抓拍记录',
            url=reverse('monitor:vehicle_search') + "?id=%s" % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        return MultipleCellDialog([record])

    operation.short_description = '操作'


@admin.register(monitor_models.VehicleMonitorDiscover)
class VehicleMonitorDiscoverAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'target', 'record', 'checked', 'detail', 'operation']
    list_filter = ['target', 'create_at']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'target': {
            'width': '120px'
        },
        'checked': {
            'width': '120px'
        }
    }

    def operation(self, model):
        detail = ModalDialog(
            cell='<el-link type="primary">查看详情</el-link>',
            title='当前数据详情',
            url=reverse('monitor:vehicle_detail') + "?id=%s" % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        back = ModalDialog(
            cell='<el-link type="primary">回放视频</el-link>',
            title='回放视频',
            url=reverse('device:video_playback') + '?id=%s' % model.id,
            height='435px',
            width='800px',
            show_cancel=True
        )
        return MultipleCellDialog([detail, back])

    operation.short_description = '操作'


@admin.register(monitor_models.RestrictedArea)
class RestrictedAreaAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'detail']
    list_filter = ['name']
    exclude = ['personnel_list']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'name': {
            'width': '160px'
        }
    }


@admin.register(monitor_models.AreaMonitorPersonnel)
class AreaMonitorPersonnelAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'area', 'personnel', 'detail']
    list_filter = ['area', 'create_at']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'area': {
            'width': '160px'
        },
        'personnel': {
            'width': '120px'
        }
    }


@admin.register(monitor_models.AreaSnapRecord)
class AreaSnapRecordAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'personnel', 'record', 'similarity']


@admin.register(monitor_models.ArchivesLibrary)
class ArchivesLibraryAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'detail']
    search_fields = ['name']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'name': {
            'width': '160px'
        }
    }


@admin.register(monitor_models.ArchivesPersonnel)
class ArchivesPersonnelAdmin(PublicModelAdmin, ImportExportModelAdmin):
    list_display = ['id', 'library', 'name', 'phone', 'id_card', 'operation']
    list_filter = ['library']
    search_fields = ['name']
    resource_class = ArchivesPersonnelResources
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'library': {
            'width': '160px'
        },
        'name': {
            'width': '120px'
        },
        'phone': {
            'width': '120px'
        },
        'id_card': {
            'width': '180px'
        }
    }

    def operation(self, model):
        trail = ModalDialog(
            cell='<el-link type="primary">轨迹档案</el-link>',
            title='轨迹档案',
            url=reverse('monitor:photo_search') + '?id=%s' % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        return MultipleCellDialog([trail])

    operation.short_description = '操作'


@admin.register(monitor_models.PhotoCluster)
class PhotoClusterAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'archives_personnel', 'device_name', 'device_address', 'device_ip', 'similarity']
    list_filter = ['archives_personnel', 'device_take_photo_time']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'archives_personnel': {
            'width': '180px'
        },
        'device_name': {
            'width': '160px'
        },
        'device_address': {
            'width': 'auto',
        },
        'device_ip': {
            'width': '120px'
        },
        'similarity': {
            'width': '100px'
        }
    }
