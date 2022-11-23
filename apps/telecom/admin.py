from django.contrib import admin
from django.utils.safestring import mark_safe
from simpleui.admin import AjaxAdmin

from telecom import models as telecom_models
from public.admin import PublicModelAdmin

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
        "percentage",
        "rate_of_attendance",
    ]
    list_filter = ["personnel_types"]

    def percentage(self, obj):
        """
        出勤百分比
        60%以下danger
        60% - 80%之间warning
        80%以上success
        """
        rate = obj.rate_of_attendance * 20
        if rate < 60:
            _types = "danger"
        elif 60 <= rate < 80:
            _types = "warning"
        elif rate >= 80:
            _types = "success"
        else:
            _types = "info"
        return mark_safe(
            f"""
            <el-tag type="{_types}">{rate}%</el-tag>
            """
        )

    percentage.short_description = "出勤百分比"
