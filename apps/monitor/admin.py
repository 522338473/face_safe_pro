import base64

import requests
from django.urls import reverse
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from simpleui.admin import AjaxAdmin
from simplepro.dialog import ModalDialog, MultipleCellDialog

from apps.device import models as device_models
from apps.monitor import models as monitor_models
from apps.monitor import serializers as monitor_serializer
from apps.public.admin import PublicModelAdmin
from apps.monitor import resources as monitor_resources
from apps.telecom import consumer
from apps.utils.constant import VIDEO_PLAY_TYPE, DETAIL_TYPE
from apps.utils.face_discern import face_discern


# Register your models here.


@admin.register(monitor_models.PersonnelType)
class PersonnelTypeAdmin(PublicModelAdmin, AjaxAdmin):
    list_display = ["id", "name", "personnel_count", "detail"]
    search_fields = ["name"]

    def personnel_count(self, obj):
        """统计改分类下人员总数"""
        return obj.monitor_set.count()

    personnel_count.short_description = "人员总数"


@admin.register(monitor_models.Monitor)
class MonitorAdmin(PublicModelAdmin, ImportExportModelAdmin, AjaxAdmin):
    list_display = [
        "id",
        "name",
        "personnel_types",
        "gender",
        "phone",
        "image",
        "operation",
    ]
    list_filter = ["personnel_types", "create_at"]
    exclude = ["num_values", "area_personnel"]
    search_fields = ["name"]
    resource_class = monitor_resources.MonitorResources
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "gender": {"width": "80px"},
        "image": {"label": "照片", "width": "120px"},
    }

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.photo
            )
        )

    image.short_description = "照片"

    def operation(self, model):
        record = ModalDialog(
            cell='<el-button type="text">抓拍记录</el-button>',
            title="抓拍记录",
            url=reverse("device:photo_search")
            + "?id={id}&detail_type={detail_type}".format(
                id=model.hash, detail_type=DETAIL_TYPE["MONITOR_DETAIL"]
            ),
            height="450px",
            width="1200px",
            show_cancel=True,
        )
        return MultipleCellDialog([record])

    operation.short_description = "操作"

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
                if result.get("error") == -1:
                    instance.set_delete()
                    self.message_user(request, "人脸注册失败")
            except Exception as e:
                instance.set_delete()
                self.message_user(request, "人脸注册失败")
            else:
                if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:
                    # 重点人员新增，ws推送
                    serializer = monitor_serializer.MonitorSerializer(instance)
                    consumer.send_message(
                        message=serializer.data, message_type="personnel_add"
                    )
        else:
            if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:
                # 重点人员修改 WS推送
                serializer = monitor_serializer.MonitorSerializer(instance)
                consumer.send_message(
                    message=serializer.data, message_type="personnel_update"
                )

    def delete_model(self, request, obj):
        """重点人员删除"""
        try:
            result = face_discern.face_warning_detect(user_id=obj.hash)
            if result.get("error") == -1:
                pass
        except Exception as e:
            pass
        else:
            if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:
                # 重点人员删除，WS推送
                serializer = monitor_serializer.MonitorSerializer(obj)
                consumer.send_message(
                    message=serializer.data, message_type="personnel_del"
                )
        finally:
            if request.user.is_superuser:
                obj.delete()
            else:
                obj.set_delete()

    def delete_queryset(self, request, queryset):

        for query in queryset:
            try:
                result = face_discern.face_warning_detect(user_id=query.hash)
                if result.get("error") == -1:
                    pass
            except Exception as e:
                pass
            else:
                if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:
                    # 重点人员删除，WS推送
                    serializer = monitor_serializer.MonitorSerializer(query)
                    consumer.send_message(
                        message=serializer.data, message_type="personnel_del"
                    )
            finally:
                if request.user.is_superuser:
                    query.delete()
                else:
                    query.set_delete()


@admin.register(monitor_models.MonitorDiscover)
class MonitorDiscoverAdmin(PublicModelAdmin, AjaxAdmin):
    list_display = [
        "id",
        "target",
        "image",
        "snap_time",
        "snap_address",
        "similarity",
        "operation",
    ]
    list_filter = ["record__take_photo_time", "target"]
    search_fields = ["target__name"]
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "image": {"width": "120px"},
    }

    def snap_time(self, obj):
        return obj.record.take_photo_time

    snap_time.short_description = "通行时间"

    def snap_address(self, obj):
        return obj.record.address

    snap_address.short_description = "通行地点"

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.record.head_path
            )
        )

    image.short_description = "抓拍人脸"

    def operation(self, model):
        detail = ModalDialog(
            cell='<el-button type="text">详情</el-button>',
            title="当前数据详情",
            url=reverse("device:photo_detail")
            + "?id={id}&detail_type={detail_type}".format(
                id=model.hash, detail_type=DETAIL_TYPE["MONITOR_DISCOVER_DETAIL"]
            ),
            height="450px",
            width="1200px",
            show_cancel=True,
        )
        back = ModalDialog(
            cell='<el-button type="text">回放视频</el-button>',
            title="回放视频",
            url=reverse("device:video_playback")
            + "?id={id}&video_play_type={video_play_type}".format(
                id=model.hash,
                video_play_type=VIDEO_PLAY_TYPE["MONITOR_DISCOVER_VIDEO_PLAY"],
            ),
            height="435px",
            width="800px",
            show_cancel=True,
        )
        return MultipleCellDialog([detail, back])

    operation.short_description = "操作"


@admin.register(monitor_models.VehicleMonitor)
class VehicleMonitorAdmin(PublicModelAdmin, ImportExportModelAdmin, AjaxAdmin):
    list_display = [
        "id",
        "plate",
        "types",
        "name",
        "gender",
        "phone",
        "id_type",
        "id_number",
        "operation",
    ]
    search_fields = ["plate", "name", "phone"]
    resource_class = monitor_resources.VehicleMonitorResources
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "plate": {"width": "120px"},
        "name": {"width": "120px"},
        "gender": {"width": "80px"},
        "phone": {"width": "120px"},
    }

    def operation(self, model):
        record = ModalDialog(
            cell='<el-button type="text">抓拍记录</el-button>',
            title="重点车辆抓拍记录",
            url=reverse("monitor:vehicle_search") + "?id={id}".format(id=model.hash),
            height="450px",
            width="1200px",
            show_cancel=True,
        )
        return MultipleCellDialog([record])

    operation.short_description = "操作"


@admin.register(monitor_models.VehicleMonitorDiscover)
class VehicleMonitorDiscoverAdmin(PublicModelAdmin, AjaxAdmin):
    list_display = ["id", "target", "image", "snap_time", "snap_address", "operation"]
    list_filter = ["target", "create_at"]
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "image": {"width": "120px"},
    }

    def snap_time(self, obj):
        return obj.record.take_photo_time

    snap_time.short_description = "通行时间"

    def snap_address(self, obj):
        return obj.record.address

    snap_address.short_description = "通行地点"

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.record.plate_path
            )
        )

    image.short_description = "抓拍照片"

    def operation(self, model):
        detail = ModalDialog(
            cell='<el-button type="text">查看详情</el-button>',
            title="当前数据详情",
            url=reverse("monitor:vehicle_detail")
            + "?id={id}&detail_type={detail_type}".format(
                id=model.hash, detail_type=DETAIL_TYPE["MONITOR_VEHICLE_DETAIL"]
            ),
            height="450px",
            width="1200px",
            show_cancel=True,
        )
        back = ModalDialog(
            cell='<el-button type="text">回放视频</el-button>',
            title="回放视频",
            url=reverse("device:video_playback")
            + "?id={id}&video_play_type={video_play_type}".format(
                id=model.hash,
                video_play_type=VIDEO_PLAY_TYPE["MONITOR_VEHICLE_VIDEO_PLAY"],
            ),
            height="435px",
            width="800px",
            show_cancel=True,
        )
        return MultipleCellDialog([detail, back])

    operation.short_description = "操作"


@admin.register(monitor_models.RestrictedArea)
class RestrictedAreaAdmin(PublicModelAdmin, AjaxAdmin):
    list_display = ["id", "name", "device", "personnel_count", "detail"]
    list_filter = ["name"]
    top_html = ' <el-alert title="门禁区域只可绑定门禁设备&无感通行! 删除门禁区域。请先删除该区域下所有人员" type="warning"></el-alert>'
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "name": {"width": "160px"},
    }

    def device(self, obj):
        device_list = []
        for item in obj.device_list.values():
            device_list.append(item.get("name"))
        return device_list

    device.short_description = "设备列表"

    def personnel_count(self, obj):
        """禁区人员统计"""
        return obj.areamonitorpersonnel_set.count()

    personnel_count.short_description = "人员总数"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        obj = super(RestrictedAreaAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )
        obj.queryset = obj.queryset.filter(device_type__in=[2, 3])  # 门禁接口只要门禁设备跟无感通行设备
        return obj


@admin.register(monitor_models.AreaMonitorPersonnel)
class AreaMonitorPersonnelAdmin(PublicModelAdmin, ImportExportModelAdmin, AjaxAdmin):
    list_display = ["id", "area", "personnel", "image", "detail"]
    list_filter = ["area", "create_at"]
    resource_class = monitor_resources.AreaMonitorPersonnelResources
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "area": {"width": "160px"},
        "personnel": {"width": "120px"},
    }

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.personnel.photo
            )
        )

    image.short_description = "照片"

    def save_model(self, request, obj, form, change):
        """新增门禁人员"""
        obj = super(AreaMonitorPersonnelAdmin, self).save_model(
            request, obj, form, change
        )
        if not change:
            b64_image = base64.b64encode(
                requests.get(url=obj.personnel.get_head_url()).content
            ).decode()
            for device in list(obj.area.device_list.values()):
                try:
                    if device.get("device_type") in (2, 3):
                        if device["device_type"] == 2:
                            ip = device["ip"]
                        elif device["device_type"] == 3:
                            ip = settings.REDIS_SERVER_HOST
                        else:
                            continue
                        message = {"name": obj.personnel.hash, "image": b64_image}
                        res = requests.post(
                            url=f"http://{ip}:5005/archives_add", json=message
                        )
                        print(res.status_code)
                        print(res.json())
                except Exception as e:
                    print(e)

    def delete_queryset(self, request, queryset):
        """删除门禁人员"""
        for query in queryset:
            for device in query.area.device_list.values():
                if device.get("device_type") in (2, 3):
                    if device["device_type"] == 2:
                        ip = device["ip"]
                    elif device["device_type"] == 3:
                        ip = settings.REDIS_SERVER_HOST
                    else:
                        continue
                    message = {"name": query.personnel.hash}
                    res = requests.post(
                        url=f"http://{ip}:5005/archives_del", json=message
                    )
                    print(res.status_code)
                    print(res.json())
        return super(AreaMonitorPersonnelAdmin, self).delete_queryset(request, queryset)


@admin.register(monitor_models.ArchivesLibrary)
class ArchivesLibraryAdmin(PublicModelAdmin, AjaxAdmin):
    list_display = ["id", "name", "personnel_count", "detail"]
    search_fields = ["name"]

    def personnel_count(self, obj):
        """统计关注人员库下人员总数"""
        return obj.archivespersonnel_set.count()

    personnel_count.short_description = "人员总数"


@admin.register(monitor_models.ArchivesPersonnel)
class ArchivesPersonnelAdmin(PublicModelAdmin, ImportExportModelAdmin, AjaxAdmin):
    list_display = ["id", "library", "name", "phone", "id_card", "image", "operation"]
    list_filter = ["library"]
    search_fields = ["name"]
    resource_class = monitor_resources.ArchivesPersonnelResources
    top_html = ' <el-alert title="关注人员隔天对前天的数据进行归档(非实时归档)!" type="warning"></el-alert>'
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "image": {"label": "抓拍人脸", "width": "120px"},
    }

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.photo
            )
        )

    image.short_description = "抓拍人脸"

    def operation(self, model):
        trail = ModalDialog(
            cell='<el-button type="text">轨迹档案</el-button>',
            title="轨迹档案",
            url=reverse("monitor:photo_search") + "?id={id}".format(id=model.hash),
            height="450px",
            width="1200px",
            show_cancel=True,
        )

        return MultipleCellDialog([trail])

    operation.short_description = "操作"

    def save_model(self, request, obj, form, change):
        """关注人员新增"""
        obj.create_by = request.user.username
        instance = super(ArchivesPersonnelAdmin, self).save_model(
            request, obj, form, change
        )
        if not change:
            try:
                image = self.get_b64_image(request)
                result = face_discern.face_focus_add(image=image, user_id=instance.hash)
                if result.get("error") == -1:
                    instance.set_delete()
                    self.message_user(request, "人脸注册失败")
            except Exception as e:
                instance.set_delete()
                self.message_user(request, "人脸注册失败")

    def delete_model(self, request, obj):
        """关注人员删除"""
        try:
            result = face_discern.face_focus_del(user_id=obj.hash)
            if result.get("error") == -1:
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
                if result.get("error") == -1:
                    pass
            except Exception as e:
                pass
            finally:
                if request.user.is_superuser:
                    query.delete()
                else:
                    query.set_delete()


@admin.register(monitor_models.PhotoCluster)
class PhotoClusterAdmin(PublicModelAdmin, AjaxAdmin):
    list_display = [
        "id",
        "archives_personnel",
        "device_name",
        "device_address",
        "device_ip",
        "device_take_photo_time",
        "similarity",
        "image",
    ]
    list_filter = ["archives_personnel", "device_take_photo_time"]
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "image": {"label": "抓拍人脸", "width": "120px"},
    }

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.device_head_path
            )
        )

    image.short_description = "抓拍人脸"
