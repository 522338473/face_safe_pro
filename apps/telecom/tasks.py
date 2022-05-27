# -*- coding: utf-8 -*-

import requests
import base64
import time
import json
from datetime import datetime, timedelta
from celery import shared_task

from django.conf import settings

from apps.telecom import models
from apps.device import models as device_models
from apps.monitor import models as monitor_models
from apps.telecom import models as telecom_models
from apps.utils.fast_dfs import upload_image
from apps.utils.job_queue import redis_queue


@shared_task
def push_algorithm(camera_ip=None, time_tag=None):
    """异步http光纤预警 /getcamera"""
    if camera_ip and time_tag:
        search_url = "".join(
            [settings.SEARCH_SERVER_HOST.replace("5000", "5001"), "/getcamera"]
        )
        response = requests.post(
            url=search_url,
            json={
                "cameraip": camera_ip,
                "timetag": time.mktime(time.strptime(time_tag, "%Y-%m-%d %H:%M:%S")),
            },
        ).json()
        if response.get("error") == 0:
            # 人脸入库
            # 数据入库
            path = upload_image(image=base64.b64decode(response["data"].get("image")))
            take_photo_time = datetime.fromtimestamp(
                response["data"].get("timetag") / 1000
            )
            detail = response["data"].get("info")
            device = device_models.DeviceInfo.objects.filter(
                delete_at__isnull=True
            ).get(ip=response["data"].get("cameraip"))
            optical = models.OpticalFiberAlarm.objects.filter(
                createAt=time_tag, devIp=camera_ip
            ).first()
            models.AlgorithmAlarm.objects.create(
                back_path=path,
                take_photo_time=take_photo_time,
                device=device,
                optical=optical,
                detail=detail,
            )

            channel_id = device.channel
            start_time_ = take_photo_time - timedelta(seconds=6)
            start_time_ = start_time_.strftime("%Y%m%d{}%H%M%S").format("T")
            params = {"channel": int(channel_id), "Starttime": str(start_time_)}
            count = 3
            while count > 0:
                try:
                    result = requests.post(
                        url="".join([settings.SEARCH_VIDEO_HOST, "/api/v1/stream/"]),
                        json=params,
                    )
                    result_json = result.json()
                except Exception as e:
                    continue
                else:
                    if (
                        result.status_code == 200
                        and result_json.get("code") == 0
                        and result_json.get("msg") == "success"
                    ):
                        break
                finally:
                    time.sleep(5)
                    count -= 1


@shared_task
def personnel_history():
    """5分钟保存历史快照"""
    redis_cache = redis_queue.redis_get_cache(redis_name="Exp")
    if redis_cache:
        # 有缓存，表示最近一轮点名未结束
        start_time = datetime.strptime(redis_cache.decode(), "%Y-%m-%d %H:%M:%S.%f")
        redis_queue.redis_set_cache(
            redis_name="Exp", redis_value=str(datetime.now()), ex=settings.EFFECTIVE
        )
    else:
        redis_queue.redis_set_cache(
            redis_name="Exp", redis_value=str(datetime.now()), ex=settings.EFFECTIVE
        )
        redis_cache = redis_queue.redis_get_cache(redis_name="Exp")
        start_time = datetime.strptime(redis_cache.decode(), "%Y-%m-%d %H:%M:%S.%f")
    f_m = timedelta(minutes=5)
    end_time = start_time + f_m
    total_person = monitor_models.Monitor.objects.filter(delete_at__isnull=True)
    attendance_person = (
        monitor_models.MonitorDiscover.objects.filter(
            delete_at__isnull=True,
            record__take_photo_time__range=(start_time, end_time),
        )
        .order_by("target", "record__take_photo_time")
        .distinct("target")
    )
    if attendance_person.exists():
        telecom_models.RollCallHistory.objects.create(
            start_time=start_time,
            end_time=end_time,
            personnel_types=total_person.last().personnel_types.name,
            total_person=total_person.count(),
            attendance_person=attendance_person.count(),
            person_list=json.dumps([item.id for item in total_person]),
            person_list_record=json.dumps([item.id for item in attendance_person]),
        )
