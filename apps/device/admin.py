from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from simplepro.dialog import ModalDialog, MultipleCellDialog

from apps.device import models as device_models
from apps.public.admin import PublicModelAdmin
from apps.utils.constant import VIDEO_PLAY_TYPE, DETAIL_TYPE
from apps.utils.job_queue import redis_queue


# Register your models here.


@admin.register(device_models.DeviceInfo)
class DeviceInfoAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "ip", "address", "status", "channel", "operation"]
    list_filter = ["name", "device_type", "create_at"]
    exclude = ["last_login", "last_logout", "snap_count", "monitor_count"]
    list_per_page = 10
    change_list_template = "admin/device/deviceinfo/change_list.html"
    change_form_template = "admin/device/deviceinfo/change_form.html"
    fields_options = {
        "id": {"fixed": "left", "width": "120px"},
        "name": {"label": "设备名称", "width": "160px"},
        "ip": {"width": "120px"},
        "address": {
            "width": "auto",
        },
        "status": {"label": "状态", "width": "100px"},
        "channel": {"label": "通道", "width": "80px"},
        "operation": {"width": "160px"},
    }

    def operation(self, model):
        login = ModalDialog(
            cell='<el-button type="text" {status}>登录</el-button>'.format(
                status="disabled" if model.status == 0 else ""
            ),
            title="摄像头登录",
            url="http://{ip}".format(ip=model.ip),
            height="80%",
            width="90%",
            show_cancel=True,
        )
        real = ModalDialog(
            cell='<el-button type="text" {status}>实况</el-button>'.format(
                status="disabled" if model.status == 0 else ""
            ),
            title="摄像头实况",
            url=reverse("device:webrtc") + "?id={id}".format(id=model.hash),
            height="430px",
            width="50%",
            show_cancel=True,
        )
        return MultipleCellDialog([login, real])

    operation.short_description = "操作"

    def save_model(self, request, obj, form, change):
        """保存数据之前做点额外的操作"""
        obj.create_by = request.user.username
        instance = super(DeviceInfoAdmin, self).save_model(request, obj, form, change)
        if instance.device_type == 0 or instance.device_type == 3:  # 普通设备触发
            if change:
                self.push_device_info(
                    ip=instance.ip,
                    rtsp_address=instance.rtsp_address,
                    device_type=instance.device_type,
                    command="del",
                )
                self.push_device_info(
                    ip=instance.ip,
                    rtsp_address=instance.rtsp_address,
                    device_type=instance.device_type,
                    command="add",
                )
            else:
                self.push_device_info(
                    ip=instance.ip,
                    rtsp_address=instance.rtsp_address,
                    device_type=instance.device_type,
                    command="add",
                )

    def delete_queryset(self, request, queryset):
        for query in queryset:
            if query.device_type == 0 or query.device_type == 3:  # 普通设备触发
                self.push_device_info(
                    ip=query.ip,
                    rtsp_address=query.rtsp_address,
                    device_type=query.device_type,
                )
            if request.user.is_superuser:
                query.delete()
            else:
                query.set_delete()

    def delete_model(self, request, obj):
        if obj.device_type == 0 or obj.device_type == 3:  # 普通设备触发
            self.push_device_info(
                ip=obj.ip, rtsp_address=obj.rtsp_address, device_type=obj.device_type
            )
        if request.user.is_superuser:
            obj.delete()
        else:
            obj.set_delete()

    @staticmethod
    def push_device_info(ip=None, rtsp_address=None, device_type=None, command=None):
        """设备rtsp流推送"""
        device_info = {"command": command, "data": [ip, rtsp_address, device_type]}
        redis_queue.device_enqueue(device_info)


@admin.register(device_models.DevicePhoto)
class DevicePhotoAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ["id", "address", "take_photo_time", "image", "operation"]
    list_filter = ["device", "take_photo_time"]
    fields_options = {
        "id": {"fixed": "left", "width": "120px"},
        "image": {"label": "抓拍人脸", "width": "120px"},
        "take_photo_time": {"width": "170px"},
        "operation": {"width": "200px"},
    }

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.head_path
            )
        )

    image.short_description = "抓拍人脸"

    def operation(self, model):
        query = ModalDialog(
            cell='<el-button type="text">查询</el-button>',
            title="抓拍记录",
            url=reverse("device:photo_search")
            + "?id={id}&detail_type={detail_type}".format(
                id=model.hash, detail_type=DETAIL_TYPE["DEVICE_PHOTO_DETAIL"]
            ),
            height="450px",
            width="1200px",
            show_cancel=True,
        )
        detail = ModalDialog(
            cell='<el-button type="text">详情</el-button>',
            title="数据详情",
            url=reverse("device:photo_detail")
            + "?id={id}&detail_type={detail_type}".format(
                id=model.hash, detail_type=DETAIL_TYPE["DEVICE_PHOTO_DETAIL"]
            ),
            height="450px",
            width="1200px",
            show_cancel=False,
        )
        back = ModalDialog(
            cell='<el-button type="text">回放视频</el-button>',
            title="回放视频",
            url=reverse("device:video_playback")
            + "?id={id}&video_play_type={video_play_type}".format(
                id=model.hash,
                video_play_type=VIDEO_PLAY_TYPE["DEVICE_PHOTO_VIDEO_PLAY"],
            ),  # 暂时写死。后期写活
            height="435px",
            width="800px",
            show_cancel=True,
        )
        return MultipleCellDialog([query, detail, back])

    operation.short_description = "操作"


@admin.register(device_models.DeviceOffLine)
class DeviceOffLineAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ["id", "device", "checked", "alarm_type", "photo_path"]
    list_filter = ["device", "create_at"]
    fields_options = {
        "id": {"fixed": "left", "width": "120px"},
        "checked": {"width": "120px"},
    }


@admin.register(device_models.Motor)
class MotorAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ["id", "device", "address", "take_photo_time", "image"]
    list_filter = ["device", "create_at"]
    fields_options = {
        "id": {"fixed": "left", "width": "120px"},
        "image": {"width": "120px"},
    }

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.motor_path
            )
        )

    image.short_description = "照片"


@admin.register(device_models.Vehicle)
class VehicleAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "device",
        "address",
        "take_photo_time",
        "plate",
        "image",
        "operation",
    ]
    list_filter = ["device", "create_at"]
    search_fields = ["plate", "color", "types"]
    fields_options = {
        "id": {"fixed": "left", "width": "120px"},
        "device": {"width": "160px"},
        "take_photo_time": {"width": "170px"},
        "plate": {"width": "100px"},
        "operation": {"width": "180px"},
    }

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.plate_path
            )
        )

    image.short_description = "照片"

    def operation(self, model):
        query = ModalDialog(
            cell='<el-button type="text">查询</el-button>',
            title="机动车搜索",
            url=reverse("device:vehicle_search") + "?id={id}".format(id=model.hash),
            height="450px",
            width="1200px",
            show_cancel=True,
        )
        detail = ModalDialog(
            cell='<el-button type="text">详情</el-button>',
            title="机动车详情",
            url=reverse("device:vehicle_detail")
            + "?id={id}&detail_type={detail_type}".format(
                id=model.hash, detail_type=DETAIL_TYPE["DEVICE_VEHICLE_DETAIL"]
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
                video_play_type=VIDEO_PLAY_TYPE["DEVICE_VEHICLE_VIDEO_PLAY"],
            ),
            height="435px",
            width="800px",
            show_cancel=True,
        )
        return MultipleCellDialog([query, detail, back])

    operation.short_description = "操作"
