# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: tasks.py
@time: 2022/4/21 15:34
"""

import json
import base64
import socket
import datetime
from celery import shared_task

from apps.device.models import DeviceInfo, DeviceOffLine
from apps.monitor.models import MonitorDiscover
from apps.utils.job_queue import redis_queue
from apps.utils.fast_dfs import upload_image


@shared_task
def device_status():
    device_result = DeviceInfo.objects.filter(delete_at__isnull=True)
    for device in device_result:
        try:
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.settimeout(0.5)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.connect((device.ip, 554))
                if device.status == 0:
                    device.device_login()
            except ConnectionRefusedError as e:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.settimeout(0.5)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.connect((device.ip, 5005))  # 门禁设备
                if device.status == 0:
                    device.device_login()
        except Exception as e:
            if device.status == 1:
                device.device_logout()
                DeviceOffLine.objects.create(device_id=device.id)
        finally:
            device.save()


@shared_task
def device_count():
    """每隔1小时同步一次"""
    device_result = DeviceInfo.objects.filter(delete_at__isnull=True)
    for device in device_result:
        try:
            device.snap_count = device.devicephoto_set.count()
            device.monitor_count = MonitorDiscover.objects.filter(
                delete_at__isnull=True,
                record__device__delete_at__isnull=True,
                record__device=device,
                record__device__name__isnull=False,
                target__area=False,
            ).count()
            device.save()
        except Exception as e:
            pass


@shared_task
def device_alarm():
    while redis_queue.redis_client.exists("redis_device_alarm"):
        alarm = json.loads(redis_queue.bl_pop_queue("redis_device_alarm", timeout=20))
        if DeviceInfo.objects.filter(
            delete_at__isnull=True, ip=alarm.get("deviceIP")
        ).exists():
            device = DeviceInfo.objects.filter(
                delete_at__isnull=True, ip=alarm.get("deviceIP")
            ).first()
            photo_path = upload_image(base64.b64decode(alarm.get("PanoramaB64")))
            alarm_type = alarm.get("alarminfo")
            create_at = datetime.datetime.fromtimestamp(alarm.get("PicTime") / 1000)
            alarm_obj = DeviceOffLine.objects.create(
                device=device, alarm_type=alarm_type, photo_path=photo_path
            )
            alarm_obj.create_at = create_at
            alarm_obj.save()
