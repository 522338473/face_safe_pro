from django.contrib import admin
from django.utils.safestring import mark_safe
from simpleui.admin import AjaxAdmin

from apps.telecom import models as telecom_models
from apps.public.admin import PublicModelAdmin

# Register your models here.


@admin.register(telecom_models.OpticalFiberAlarm)
class OpticalFiberAlarmAdmin(PublicModelAdmin, AjaxAdmin):
    """光纤报警"""

    list_display = [
        "id",
        "position",
        "createAt",
        "geo",
        "channel",
        "devIp",
        "alarmType",
    ]
    list_filter = ["devIp", "alarmType"]


@admin.register(telecom_models.AlgorithmAlarm)
class AlgorithmAlarmAdmin(PublicModelAdmin, AjaxAdmin):
    """算法报警"""

    list_display = ["id", "device", "optical", "image", "take_photo_time"]
    list_filter = ["device", "take_photo_time"]

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.back_path
            )
        )

    image.short_description = "背景抓拍"


@admin.register(telecom_models.RollCallHistory)
class RollCallHistoryAdmin(PublicModelAdmin, AjaxAdmin):
    """历史点名"""

    list_display = [
        "id",
        "start_time",
        "end_time",
        "personnel_types",
        "total_person",
        "attendance_person",
        "rate_of_attendance",
    ]
    list_filter = ["personnel_types"]
