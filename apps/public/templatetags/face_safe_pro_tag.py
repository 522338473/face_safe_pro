# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: face_safe_pro_tag.py
@time: 2022/3/14 17:49
"""
import datetime
from functools import wraps

from django.core.paginator import Paginator
from django.utils.safestring import mark_safe, SafeData
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncHour

from device import models as device_model
from archives import models as archives_model
from monitor import models as monitor_model
from public.templatetags import register
from utils.hasher import Hasher


@register.simple_tag
def device_status():
    """
    :return: 摄像头状态
    """
    return (
        device_model.DeviceInfo.objects.values("status")
        .annotate(count=Count("status"))
        .values("status", "count")
    )


@register.simple_tag
def device_info(*args, **kwargs):
    """
    :return: 摄像头分布|列表
    """
    current_page = kwargs.get("current_page", 1)
    page_size = kwargs.get("page_size", 10)
    device_page = Paginator(
        device_model.DeviceInfo.objects.values(
            "name", "ip", "status", "address", "geo"
        ).order_by("id"),
        page_size,
    )
    if device_page.page_range.start <= current_page < device_page.page_range.stop:
        return {
            "device_page": device_page,
            "device_list": device_page.page(current_page).object_list,
        }


@register.simple_tag
def survey():
    """
    首页概况
    :return:
    now_days_snap_total: 今日抓拍
    all_days_snap_total: 总抓拍
    monitor_total: 重点人员
    personnel_total: 关注人员
    archives_total: 人员档案
    """
    now_days_snap_total = device_model.DevicePhoto.objects.filter(
        take_photo_time__gte=datetime.datetime.now().date()
    ).count()
    all_days_snap_total = device_model.DevicePhoto.objects.count()
    monitor_total = monitor_model.Monitor.objects.count()
    personnel_total = monitor_model.ArchivesPersonnel.objects.count()
    archives_total = archives_model.Personnel.objects.count()
    data = {
        "now_days_snap_total": now_days_snap_total,
        "all_days_snap_total": all_days_snap_total,
        "monitor_total": monitor_total,
        "personnel_total": personnel_total,
        "archives_total": archives_total,
    }
    return data


@register.simple_tag
def snap_count(*args, **kwargs):
    """
    抓拍统计
    :param args: 位置参数
    :param kwargs: 关键字参数 {% snap_count start='2021' end='2023' %}
    :return:
    # 可根据ExtractDay进行分组返回
    from django.db.models.functions import ExtractDay, ExtractHour
    face_list_1 = face_query.annotate(day=ExtractDay('take_photo_time')).values('day').annotate(count=Count('id')).values('day', 'count')
    face_list_2 = face_query.annotate(hour=ExtractHour('take_photo_time')).values('hour').annotate(count=Count('id')).values('hour', 'count')
    """
    start_time = kwargs.get("start_time", None)
    end_time = kwargs.get("end_time", None)
    days = datetime.timedelta(days=1)
    try:
        start_date = datetime.datetime.strptime(start_time, "%Y%m%d%H%M%S")
        end_date = datetime.datetime.strptime(end_time, "%Y%m%d%H%M%S")
    except ValueError:
        start_date = datetime.datetime.strptime(
            datetime.datetime.now().date().strftime("%Y%m%d%H%M%S"), "%Y%m%d%H%M%S"
        )
        end_date = datetime.datetime.strptime(
            datetime.datetime.now().strftime("%Y%m%d%H%M%S"), "%Y%m%d%H%M%S"
        )
    count_list = {
        "dates": {
            "start_date": start_date.strftime("%Y%m%d%H%M%S"),
            "end_date": end_date.strftime("%Y%m%d%H%M%S"),
        },
        "people_count": [],
        "vehicle_count": [],
    }
    face_query = device_model.DevicePhoto.objects.all()
    vehicle_query = device_model.Vehicle.objects.all()

    if end_date - start_date <= days:
        face_list = (
            face_query.filter(take_photo_time__range=(start_date, end_date))
            .annotate(date=TruncHour("take_photo_time"))
            .values("date")
            .annotate(count=Count("date"))
            .order_by()
        )
        vehicle_list = (
            vehicle_query.filter(take_photo_time__range=(start_date, end_date))
            .annotate(date=TruncHour("take_photo_time"))
            .values("date")
            .annotate(count=Count("date"))
            .order_by()
        )
        for face in face_list:
            count_list["people_count"].append(
                {"date": face["date"].strftime("%Y-%m-%d %H"), "count": face["count"]}
            )
        for vehicle in vehicle_list:
            count_list["vehicle_count"].append(
                {
                    "date": vehicle["date"].strftime("%Y-%m-%d %H"),
                    "count": vehicle["count"],
                }
            )
    else:
        face_list = (
            face_query.filter(take_photo_time__range=(start_date, end_date))
            .annotate(date=TruncDay("take_photo_time"))
            .values("date")
            .annotate(count=Count("date"))
            .order_by()
        )
        vehicle_list = (
            vehicle_query.filter(take_photo_time__range=(start_date, end_date))
            .annotate(date=TruncDay("take_photo_time"))
            .values("date")
            .annotate(count=Count("date"))
            .order_by()
        )
        for face in face_list:
            count_list["people_count"].append(
                {"date": face["date"].strftime("%Y-%m-%d"), "count": face["count"]}
            )
        for vehicle in vehicle_list:
            count_list["vehicle_count"].append(
                {
                    "date": vehicle["date"].strftime("%Y-%m-%d"),
                    "count": vehicle["count"],
                }
            )

    return count_list


@register.simple_tag
def alarm_count():
    """
    :return: 预警统计
    monitor_discovery_total: 重点人员
    vehicle_discovery_total: 重点车辆
    area_discovery_total: 区域报警
    """
    monitor_discovery_total = monitor_model.MonitorDiscover.objects.filter(
        target__area=False
    ).count()
    vehicle_discovery_total = monitor_model.VehicleMonitorDiscover.objects.count()
    area_discovery_total = monitor_model.MonitorDiscover.objects.filter(
        target__area=True
    ).count()

    data = {
        "monitor_discovery_total": monitor_discovery_total,
        "vehicle_discovery_total": vehicle_discovery_total,
        "area_discovery_total": area_discovery_total,
    }
    return data


@register.simple_tag
def alarm_unchecked_count():
    """
    :return: 预警统计 | 所有未读
    monitor_discovery_total: 重点人员
    vehicle_discovery_total: 重点车辆
    area_discovery_total: 区域报警
    """
    monitor_discovery_total = monitor_model.MonitorDiscover.objects.filter(
        target__area=False, checked=False
    ).count()
    vehicle_discovery_total = monitor_model.VehicleMonitorDiscover.objects.filter(
        checked=False
    ).count()
    area_discovery_total = monitor_model.MonitorDiscover.objects.filter(
        target__area=True, checked=False
    ).count()

    data = {
        "monitor_discovery_total": monitor_discovery_total,
        "vehicle_discovery_total": vehicle_discovery_total,
        "area_discovery_total": area_discovery_total,
    }
    return data


@register.simple_tag
def alarm_list(*args, **kwargs):
    """预警"""
    current_page = kwargs.get("current_page", 1)
    page_size = kwargs.get("page_size", 10)
    alarm_page = Paginator(
        monitor_model.MonitorDiscover.objects.order_by(
            "record__take_photo_time"
        ).values("id", "target__name", "target__photo", "record__head_path"),
        page_size,
    )
    if alarm_page.page_range.start <= current_page < alarm_page.page_range.stop:
        return {
            "alarm_page": alarm_page,
            "alarm_list": alarm_page.page(current_page).object_list,
        }


@register.simple_tag
def alarm_message():
    """预警信息|告警通知"""
    pass


@register.simple_tag
def archives_count():
    """
    档案统计|人数统计
    :return:
    """
    archives_group_total = archives_model.ArchivesGroup.objects.count()
    archives_personnel_total = archives_model.Personnel.objects.count()
    data = {
        "archives_group_total": archives_group_total,
        "archives_personnel_total": archives_personnel_total,
    }
    return data


@register.simple_tag
def device_snap_count():
    """
    设备抓拍统计
    :return:
    """
    now_days_snap_total = device_model.DevicePhoto.objects.filter(
        take_photo_time__gte=datetime.datetime.now().date()
    ).count()
    all_days_snap_total = device_model.DevicePhoto.objects.count()
    data = {
        "now_days_snap_total": now_days_snap_total,
        "all_days_snap_total": all_days_snap_total,
    }
    return data


@register.simple_tag
def video_live(*args, **kwargs):
    """
    视频实况
    :param args:
    :param kwargs:
    :return:
    """
    _hash = kwargs.get("id")
    device_ = device_model.DeviceInfo.objects.get(id=Hasher.to_object_pk(_hash))
    # return device_.rtsp_address
    return "http://192.168.2.95:8083/stream/f1ddee0d7cf3a88f42b958a4053ea566/channel/0/webrtc?uuid=f1ddee0d7cf3a88f42b958a4053ea566&channel=0"


@register.simple_tag
def device_photo_list(*args, **kwargs):
    """
    当前设备抓拍
    :param args:
    :param kwargs:
    :return: 分页器返回
    """
    _hash = kwargs.get("id")
    current_page = kwargs.get("current_page", 1)
    page_size = kwargs.get("page_size", 10)
    device_page = Paginator(
        device_model.DevicePhoto.objects.filter(
            device__id=Hasher.to_object_pk(_hash)
        ).order_by("-id"),
        page_size,
    )
    if device_page.page_range.start <= current_page < device_page.page_range.stop:
        return {
            "device_page": device_page,
            "device_photo_list": device_page.page(current_page).object_list,
        }


@register.simple_tag
def archives_group(*args, **kwargs):
    """档案库列表"""
    current_page = kwargs.get("current_page", 1)
    page_size = kwargs.get("page_size", 10)
    archives_group_page = Paginator(
        archives_model.ArchivesGroup.objects.order_by("id"), page_size
    )
    if (
        archives_group_page.page_range.start
        <= current_page
        < archives_group_page.page_range.stop
    ):
        return {
            "archives_group_page": archives_group_page,
            "archives_list": archives_group_page.page(current_page).object_list,
        }


@register.simple_tag
def archives_personnel(*args, **kwargs):
    """
    档案人员列表
    :param args:
    :param kwargs: 不传id表示查看所有人员。默认一页显示10条
    :return:
    """
    _hash = kwargs.get("id")
    current_page = kwargs.get("current_page", 1)
    page_size = kwargs.get("page_size", 10)
    if _hash:
        personnel_page = Paginator(
            archives_model.Personnel.objects.filter(
                archives_group_id=Hasher.to_object_pk(_hash)
            ).order_by("-id"),
            page_size,
        )
    else:
        personnel_page = Paginator(
            archives_model.Personnel.objects.order_by("-id"), page_size
        )
    if personnel_page.page_range.start <= current_page < personnel_page.page_range.stop:
        return {
            "personnel_page": personnel_page,
            "personnel_list": personnel_page.page(current_page).object_list,
        }


def stringfilter(func):
    """
    Decorator for filters which should only receive strings. The object
    passed as the first positional argument will be converted to a string.
    """

    def _dec(*args, **kwargs):
        args = list(args)
        args[0] = str(args[0])
        if isinstance(args[0], SafeData) and getattr(
            _dec._decorated_function, "is_safe", False
        ):
            return mark_safe(func(*args, **kwargs))
        return func(*args, **kwargs)

    # Include a reference to the real function (used to check original
    # arguments by the template parser, and to bear the 'is_safe' attribute
    # when multiple decorators are applied).
    _dec._decorated_function = getattr(func, "_decorated_function", func)

    return wraps(func)(_dec)


@register.filter(is_safe=True)
@stringfilter
def safe_q(value):
    """Mark the value as a string that should not be auto-escaped."""
    value = value.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
    return mark_safe(value)
