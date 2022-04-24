from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from simplepro.dialog import ModalDialog, MultipleCellDialog

from apps.monitor import models as monitor_models
from apps.public.admin import PublicModelAdmin
from apps.public.resources import MonitorResources, ArchivesPersonnelResources
from apps.utils.constant import VIDEO_PLAY_TYPE, DETAIL_TYPE
from apps.utils.face_discern import face_discern


# Register your models here.


@admin.register(monitor_models.PersonnelType)
class PersonnelTypeAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'detail']
    search_fields = ['name']


@admin.register(monitor_models.Monitor)
class MonitorAdmin(PublicModelAdmin, ImportExportModelAdmin):
    list_display = ['id', 'name', 'personnel_types', 'gender', 'phone', 'image', 'operation']
    list_filter = ['personnel_types', 'create_at']
    exclude = ['num_values', 'area_personnel']
    search_fields = ['name']
    resource_class = MonitorResources
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'gender': {
            'width': '80px'
        },
        'image': {
            'label': '照片',
            'width': '120px'
        },

    }

    def image(self, obj):
        return mark_safe('<img src={url} width=30px;>'.format(url=obj.photo))

    image.short_description = '照片'

    def operation(self, model):
        record = ModalDialog(
            cell='<el-button type="text">抓拍记录</el-button>',
            title='抓拍记录',
            url=reverse('device:photo_search') + "?id={id}&detail_type={detail_type}".format(id=model.hash, detail_type=DETAIL_TYPE['MONITOR_DETAIL']),
            height='450px',
            width='1200px',
            show_cancel=True
        )
        return MultipleCellDialog([record])

    operation.short_description = '操作'

    def save_model(self, request, obj, form, change):
        """重点人员新增"""
        obj.create_by = request.user.username
        instance = super(MonitorAdmin, self).save_model(request, obj, form, change)
        if not change:
            try:
                image = self.get_b64_image(request)
                result = face_discern.face_warning_add(
                    image=image, user_id=instance.hash
                )
                if result.get('error') == -1:
                    instance.set_delete()
                    self.message_user(request, '人脸注册失败')
            except Exception as e:
                instance.set_delete()
                self.message_user(request, '人脸注册失败')

    def delete_model(self, request, obj):
        """重点人员删除"""
        try:
            result = face_discern.face_warning_detect(user_id=obj.hash)
            if result.get('error') == -1:
                pass
        except Exception as e:
            pass
        finally:
            if request.user.is_superuser:
                obj.delete()
            else:
                obj.set_delete()

    def delete_queryset(self, request, queryset):

        for query in queryset:
            try:
                result = face_discern.face_warning_detect(user_id=query.hash)
                if result.get('error') == -1:
                    pass
            except Exception as e:
                pass
            finally:
                if request.user.is_superuser:
                    query.delete()
                else:
                    query.set_delete()


@admin.register(monitor_models.MonitorDiscover)
class MonitorDiscoverAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'target', 'image', 'checked', 'similarity', 'operation']
    list_filter = ['record__take_photo_time', 'target']
    search_fields = ['target__name']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'image': {
            'width': '120px'
        }
    }

    def image(self, obj):
        return mark_safe('<img src={url} width=30px;>'.format(url=obj.record.head_path))

    image.short_description = '抓拍人脸'

    def operation(self, model):
        detail = ModalDialog(
            cell='<el-button type="text">详情</el-button>',
            title='当前数据详情',
            url=reverse('device:photo_detail') + "?id={id}&detail_type={detail_type}".format(id=model.hash, detail_type=DETAIL_TYPE['MONITOR_DISCOVER_DETAIL']),
            height='450px',
            width='1200px',
            show_cancel=True
        )
        back = ModalDialog(
            cell='<el-button type="text">回放视频</el-button>',
            title='回放视频',
            url=reverse('device:video_playback') + '?id={id}&video_play_type={video_play_type}'.format(id=model.hash, video_play_type=VIDEO_PLAY_TYPE['MONITOR_DISCOVER_VIDEO_PLAY']),
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
            cell='<el-button type="text">抓拍记录</el-button>',
            title='重点车辆抓拍记录',
            url=reverse('monitor:vehicle_search') + "?id={id}".format(id=model.hash),
            height='450px',
            width='1200px',
            show_cancel=True
        )
        return MultipleCellDialog([record])

    operation.short_description = '操作'


@admin.register(monitor_models.VehicleMonitorDiscover)
class VehicleMonitorDiscoverAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'target', 'image', 'checked', 'detail', 'operation']
    list_filter = ['target', 'create_at']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'image': {
            'width': '120px'
        }
    }

    def image(self, obj):
        return mark_safe('<img src={url} width=30px;>'.format(url=obj.record.plate_path))

    image.short_description = '抓拍照片'

    def operation(self, model):
        detail = ModalDialog(
            cell='<el-button type="text">查看详情</el-button>',
            title='当前数据详情',
            url=reverse('monitor:vehicle_detail') + "?id={id}&detail_type={detail_type}".format(id=model.hash, detail_type=DETAIL_TYPE['MONITOR_VEHICLE_DETAIL']),
            height='450px',
            width='1200px',
            show_cancel=True
        )
        back = ModalDialog(
            cell='<el-button type="text">回放视频</el-button>',
            title='回放视频',
            url=reverse('device:video_playback') + '?id={id}&video_play_type={video_play_type}'.format(id=model.hash, video_play_type=VIDEO_PLAY_TYPE['MONITOR_VEHICLE_VIDEO_PLAY']),
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
    list_display = ['id', 'library', 'name', 'phone', 'id_card', 'image', 'operation']
    list_filter = ['library']
    search_fields = ['name']
    resource_class = ArchivesPersonnelResources
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'image': {
            'label': '抓拍人脸',
            'width': '120px'
        },
    }

    def image(self, obj):
        return mark_safe('<img src={url} width=30px;>'.format(url=obj.photo))

    image.short_description = '抓拍人脸'

    def operation(self, model):
        trail = ModalDialog(
            cell='<el-button type="text">轨迹档案</el-button>',
            title='轨迹档案',
            url=reverse('monitor:photo_search') + '?id={id}'.format(id=model.hash),
            height='450px',
            width='1200px',
            show_cancel=True
        )

        return MultipleCellDialog([trail])

    operation.short_description = '操作'

    def save_model(self, request, obj, form, change):
        """关注人员新增"""
        obj.create_by = request.user.username
        instance = super(ArchivesPersonnelAdmin, self).save_model(request, obj, form, change)
        if not change:
            try:
                image = self.get_b64_image(request)
                result = face_discern.face_focus_add(
                    image=image, user_id=instance.hash
                )
                if result.get('error') == -1:
                    instance.set_delete()
                    self.message_user(request, '人脸注册失败')
            except Exception as e:
                instance.set_delete()
                self.message_user(request, '人脸注册失败')

    def delete_model(self, request, obj):
        """关注人员删除"""
        try:
            result = face_discern.face_focus_del(user_id=obj.hash)
            if result.get('error') == -1:
                pass
        except Exception as e:
            pass
        finally:
            if request.user.is_superuser:
                obj.delete()
            else:
                obj.set_delete()

    def delete_queryset(self, request, queryset):
        for query in queryset:
            try:
                result = face_discern.face_focus_del(user_id=query.hash)
                if result.get('error') == -1:
                    pass
            except Exception as e:
                pass
            finally:
                if request.user.is_superuser:
                    query.delete()
                else:
                    query.set_delete()


@admin.register(monitor_models.PhotoCluster)
class PhotoClusterAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'archives_personnel', 'device_name', 'device_address', 'device_ip', 'device_take_photo_time', 'similarity', 'image']
    list_filter = ['archives_personnel', 'device_take_photo_time']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'image': {
            'label': '抓拍人脸',
            'width': '120px'
        }
    }

    def image(self, obj):
        return mark_safe('<img src={url} width=30px;>'.format(url=obj.device_head_path))

    image.short_description = '抓拍人脸'
