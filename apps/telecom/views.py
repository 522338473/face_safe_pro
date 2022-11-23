import hashlib
import time

import requests
import datetime
import json

from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from django.conf import settings

from public.views import HashRetrieveViewSetMixin

from telecom import models
from telecom import serializers
from telecom import tasks
from device import models as device_models
from device import serializers as device_serializers
from monitor import models as monitor_models
from monitor import serializers as monitor_serializer
from utils.job_queue import redis_queue


"""
1. 光纤报警新增(异步推送算法)
2. 光纤报警列表(查看最近设备实况视频)
3. 算法报警列表
4. 算法报警详情(20秒视频回放)
5. 实时视频流
"""


class OpticalFiberAlarmViewSet(
    HashRetrieveViewSetMixin, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """
    光纤报警
    """

    queryset = models.OpticalFiberAlarm.objects.filter(delete_at__isnull=True).order_by(
        "-create_at"
    )
    serializer_class = serializers.OpticalFiberAlarmSerializer
    permission_classes = [
        AllowAny,
    ]

    def list(self, request, *args, **kwargs):
        """
        光纤报警列表
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        光纤推送报警，异步告知算法
        """
        request_data = request.data
        # camera_ip = self.get_device_ip_by_channel(channel=request_data.get('channel'))
        create_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        camera_ip = self.get_device_ip_by_position(
            position=request_data.get("position")
        )
        if not camera_ip:
            raise ParseError("不在报警范围内.")
        request_data["devIp"] = camera_ip
        request_data["createAt"] = create_at
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        tasks.push_algorithm.delay(camera_ip=camera_ip, time_tag=create_at)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @staticmethod
    def get_device_ip_by_channel(channel=None):
        """根据通道号获取设备ip"""
        channel_dict = {"1": "192.168.2.247", "2": "192.168.2.248"}
        if isinstance(channel, int):
            return channel_dict[str(channel)]

    @staticmethod
    def get_device_ip_by_position(position=None):
        """根据报警位置获取设备ip"""
        position_list = [(0, 10, "192.168.2.247"), (950, 1051, "192.168.2.248")]
        if isinstance(position, str):
            for item in position_list:
                if int(position) in range(item[0], item[1]):
                    return item[2]

    @action(methods=["POST", "GET"], detail=False, url_path="push_waterfall")
    def push_waterfall(self, request, *args, **kwargs):
        """瀑布图推送接口"""
        alarm_data = request.data
        # alarm.put_queue(data=alarm_data)
        redis_queue.redis_set_cache(
            redis_name="WATERFALL", redis_value=json.dumps(alarm_data)
        )
        return Response(alarm_data)

    @action(methods=["GET"], detail=False, url_path="get_waterfall")
    def get_waterfall(self, request, *args, **kwargs):
        """获取瀑布图数据"""
        # return Response(alarm.get_queue())
        data = redis_queue.redis_get_cache(redis_name="WATERFALL")
        if data is not None:
            data = json.loads(data.decode())
        return Response(data)


class AlgorithmAlarmViewSet(
    HashRetrieveViewSetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """
    算法报警
    """

    queryset = models.AlgorithmAlarm.objects.filter(delete_at__isnull=True).order_by(
        "-create_at"
    )
    serializer_class = serializers.AlgorithmAlarmSerializer
    permission_classes = [
        AllowAny,
    ]

    def list(self, request, *args, **kwargs):
        """
        算法报警列表
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        算法报警详情
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="video_playback")
    def video_playback(self, request, *args, **kwargs):
        """回放视频"""

        channel_id = request.query_params.get("channel_id", None)
        take_time = request.query_params.get("take_time", None)

        if not channel_id or not take_time:
            return Response({"message": "参数缺失"})
        try:
            try:
                start_time_ = datetime.datetime.strptime(
                    take_time, "%Y-%m-%d %H:%M:%S"
                ) - datetime.timedelta(seconds=6)
            except ValueError:
                start_time_ = datetime.datetime.strptime(
                    take_time, "%Y-%m-%d %H:%M:%S"
                ) - datetime.timedelta(seconds=6)
            start_time_ = start_time_.strftime("%Y%m%d{}%H%M%S").format("T")
        except ValueError:
            raise ParseError("时间格式错误")

        params = {"channel": int(channel_id), "Starttime": str(start_time_)}
        try:
            result = requests.post(
                url="".join([settings.SEARCH_VIDEO_HOST, "/api/v1/stream/"]),
                json=params,
            )
            result_json = result.json()
        except requests.exceptions.ConnectionError:
            return Response({"message": "录像机数据获取错误"})
        except Exception as e:
            print(e)
            return Response({"message": "数据处理失败"})
        if (
            result.status_code == 200
            and result_json.get("code") == 0
            and result_json.get("msg") == "success"
        ):
            photo_id = result_json.get("data")["id"]

            result = {
                "url": "".join(
                    [settings.VIDEO_HOST, "/mp4/{id}/stream.mp4".format(id=photo_id)]
                )
            }
            return Response(result)
        else:
            return Response({"message": result_json.get("msg")})

    @action(methods=["GET"], detail=True, url_path="video")
    def video(self, request, *args, **kwargs):
        """实时视频流"""
        instance = self.get_object()
        device_instance = device_models.DeviceInfo.objects.filter(
            delete_at__isnull=True
        ).get(ip=instance.device.ip)

        if device_instance.status == 0:
            return Response({"message": "设备离线"})

        if not device_instance.rtsp_address:
            return Response({"message": "缺少rtsp地址"})

        stream_uuid = hashlib.md5(
            "_".join([device_instance.ip, device_instance.rtsp_address]).encode("utf-8")
        ).hexdigest()
        data = {
            "uuid": stream_uuid,
            "name": device_instance.name,
            "channels": {
                "0": {
                    "url": device_instance.rtsp_address,
                    "on_demand": True,
                    "debug": False,
                }
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
                return Response(
                    {
                        "url": "".join(
                            [
                                settings.SEARCH_REAL_TIME_HOST,
                                "/stream/{stream}/channel/{channel}/webrtc?uuid={stream}&channel={channel}".format(
                                    stream=stream_uuid, channel=0
                                ),
                            ]
                        )
                    }
                )
        except requests.exceptions.ConnectionError:
            raise ParseError("无法与RTSP服务建立正常链接.")
        except Exception as e:
            raise ParseError("服务器异常")


class DeviceInfoViewSet(HashRetrieveViewSetMixin, mixins.ListModelMixin):

    queryset = device_models.DeviceInfo.objects.filter(delete_at__isnull=True).order_by(
        "create_at"
    )
    serializer_class = device_serializers.DeviceInfoSerializers

    def list(self, request, *args, **kwargs):
        """摄像头列表"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="offline")
    def offline(self, request, *args, **kwargs):
        """设备离线记录"""
        queryset = device_models.DeviceOffLine.objects.order_by("-create_at")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = device_serializers.DeviceOffLineSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = device_serializers.DeviceOffLineSerializers(page, many=True)
        return Response(serializer.data)


class PersonnelTypeViewSet(
    HashRetrieveViewSetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin
):

    queryset = monitor_models.PersonnelType.objects.filter(delete_at__isnull=True)
    serializer_class = monitor_serializer.PersonnelTypeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = models.RollCallHistory.objects.filter(
            personnel_types=instance.name
        ).order_by("-create_at")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.RollCallHistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.RollCallHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class MonitorViewSet(HashRetrieveViewSetMixin, mixins.ListModelMixin):
    """重点人员"""

    queryset = monitor_models.Monitor.objects.filter(delete_at__isnull=True).order_by(
        "-create_at"
    )
    serializer_class = monitor_serializer.MonitorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MonitorDiscoveryViewSet(
    HashRetrieveViewSetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """重点人员通行记录"""

    queryset = monitor_models.MonitorDiscover.objects.filter(
        delete_at__isnull=True
    ).order_by("target", "record__take_photo_time")
    serializer_class = monitor_serializer.MonitorDiscoverSerializer

    def filter_queryset(self, queryset):
        redis_cache = redis_queue.redis_get_cache(redis_name="Exp")
        if redis_cache:
            # 有缓存，表示最近一轮点名未结束
            start_time = datetime.datetime.strptime(
                redis_cache.decode(), "%Y-%m-%d %H:%M:%S.%f"
            )
        else:
            # 无缓存，表示即将开始新一轮，设置缓存
            redis_queue.redis_set_cache(
                redis_name="Exp",
                redis_value=str(datetime.datetime.now()),
                ex=settings.EFFECTIVE,
            )
            redis_cache = redis_queue.redis_get_cache(redis_name="Exp")
            start_time = datetime.datetime.strptime(
                redis_cache.decode(), "%Y-%m-%d %H:%M:%S.%f"
            )
        f_m = datetime.timedelta(minutes=5)
        end_time = start_time + f_m
        queryset = queryset.filter(
            record__take_photo_time__range=(start_time, end_time)
        ).distinct("target")

        return super(MonitorDiscoveryViewSet, self).filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RollCallHistoryViewSet(
    HashRetrieveViewSetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    """
    点名系统
    """

    queryset = models.RollCallHistory.objects.order_by("-create_at")
    serializer_class = serializers.RollCallHistorySerializer

    def list(self, request, *args, **kwargs):
        """
        查看快照列表
        """
        queryset = self.filter_queryset(self.get_queryset())
        paginate = request.query_params.get("paginate", None)
        if paginate == "off":
            serializer = self.get_serializer(queryset, many=True)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        获取到当前实例，数据库查询返回记录
        """
        instance = self.get_object()
        id = instance.hash
        total_person = instance.total_person
        attendance_person = instance.attendance_person
        rate_of_attendance = instance.rate_of_attendance
        personnel_types = instance.personnel_types
        person_list = json.loads(instance.person_list)
        person_list_query = list(
            monitor_models.Monitor.objects.in_bulk(person_list).values()
        )
        person_list_serializer = monitor_serializer.MonitorSerializer(
            person_list_query, many=True
        )

        person_list_record = json.loads(instance.person_list_record)
        person_list_record_query = list(
            monitor_models.MonitorDiscover.objects.in_bulk(person_list_record).values()
        )
        person_list_record_serializer = monitor_serializer.MonitorDiscoverSerializer(
            person_list_record_query, many=True
        )
        return Response(
            {
                "id": id,
                "total_person": total_person,
                "attendance_person": attendance_person,
                "rate_of_attendance": rate_of_attendance,
                "personnel_types": personnel_types,
                "person_list": person_list_serializer.data,
                "person_list_record": person_list_record_serializer.data,
            }
        )

    @action(methods=["GET"], detail=False, url_path="exp_time")
    def exp_time(self, request, *args, **kwargs):
        """返回最近一次点名区间"""
        redis_cache = redis_queue.redis_get_cache(redis_name="Exp")
        if redis_cache:
            # 有缓存，表示最近一轮点名未结束
            start_time = datetime.datetime.strptime(
                redis_cache.decode(), "%Y-%m-%d %H:%M:%S.%f"
            )
        else:
            # 无缓存，表示即将开始新一轮，设置缓存
            redis_queue.redis_set_cache(
                redis_name="Exp",
                redis_value=str(datetime.datetime.now()),
                ex=settings.EFFECTIVE,
            )
            start_time = str(datetime.datetime.now())
        f_m = datetime.timedelta(minutes=5)
        end_time = start_time + f_m
        now_time = datetime.datetime.now()
        return Response(
            {
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "remaining_time": (end_time - now_time).seconds,
            }
        )
