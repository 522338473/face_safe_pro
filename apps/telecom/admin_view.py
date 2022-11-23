# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: admin_view.py
@time: 2022/4/7 10:58
"""
import datetime

import requests
import hashlib

from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response

from device import models as device_models
from public.views import ParseJsonView


# Create your views here.


class FibreOpticalView(ParseJsonView, View):
    """光纤大屏页面"""

    def get(self, request, *args, **kwargs):
        return render(request, "admin/telecom/fibre_optical.html")


class RollCallView(ParseJsonView, View):
    """点名系统大屏页面"""

    def get(self, request, *args, **kwargs):
        return render(request, "admin/telecom/roll_call.html")


class HistoryView(ParseJsonView, View):
    """点名系统历史记录"""

    def get(self, request, *args, **kwargs):
        return render(request, "admin/telecom/history.html")


class VideoPlaybackView(ParseJsonView, View):
    """回放视频View"""

    def post(self, request):
        """返回视频url"""
        _id = request.POST.get("id")
        photo_obj = device_models.DevicePhoto.objects.get(id=self.hash_to_pk(_id))
        start_time = (
            photo_obj.take_photo_time - datetime.timedelta(seconds=5)
        ).strftime("%Y%m%dT%H%M%S")
        channel = photo_obj.device.channel
        params = {"channel": int(channel), "Starttime": str(start_time)}
        try:
            result = requests.post(
                url="".join([settings.SEARCH_VIDEO_HOST, "/api/v1/stream/"]),
                json=params,
            )
            result_json = result.json()
        except Exception as e:
            return JsonResponse({"message": "录像机数据获取失败"})
        if (
            result.status_code == 200
            and result_json.get("code") == 0
            and result_json.get("msg") == "success"
        ):
            photo_id = result_json.get("data")["id"]
            url = "".join(
                [settings.VIDEO_HOST, "/mp4/{id}/stream.mp4".format(id=photo_id)]
            )
            return JsonResponse({"url": url})
        else:
            return JsonResponse({"message": result_json.get("msg")})


class WebRtcView(ParseJsonView, View):
    """单摄像头webrtc视频流"""

    def get(self, request):
        _id = request.GET.get("id")
        device_obj = device_models.DeviceInfo.objects.get(id=self.hash_to_pk(_id))
        if device_obj.status == 0:
            return Response({"message": "设备离线"})
        if not device_obj.rtsp_address:
            return Response({"message": "缺少rtsp地址"})
        stream_uuid = hashlib.md5(
            "_".join([device_obj.ip, device_obj.rtsp_address]).encode("utf-8")
        ).hexdigest()

        data = {
            "uuid": stream_uuid,
            "name": device_obj.name,
            "channels": {
                "0": {"url": device_obj.rtsp_address, "on_demand": True, "debug": False}
            },
        }

        try:
            res = requests.post(
                url="".join(
                    [
                        settings.SEARCH_REAL_TIME_HOST,
                        "/stream/{stream}/add".format(stream=stream_uuid),
                    ]
                ),
                json=data,
                auth=("demo", "demo"),
            )
            if res.json():
                device_video_url = "".join(
                    [
                        settings.SEARCH_REAL_TIME_HOST,
                        "/stream/{stream}/channel/{channel}/webrtc?uuid={stream}&channel={channel}".format(
                            stream=stream_uuid, channel=0
                        ),
                    ]
                )
        except Exception as e:
            raise
        return render(request, "admin/device/other/webrtc.html", locals())
