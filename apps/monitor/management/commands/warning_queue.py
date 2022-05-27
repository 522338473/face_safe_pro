# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: warning_queue.py
@time: 2021/12/10 20:30
"""

import logging
import base64
import json
import requests
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.monitor import models as monitor_models
from apps.monitor import serializers as monitor_serializers
from apps.utils.face_discern import face_discern
from apps.utils.job_queue import redis_queue
from apps.utils.hasher import Hasher
from apps.monitor import tasks
from apps.telecom import consumer


logger = logging.getLogger("server.default")


class Command(BaseCommand):
    help = "Get the warning result from the redis queue"

    def handle(self, *args, **options):
        print("warning queue result start!")
        while 1:
            self.warning_queue()

    @staticmethod
    def mapper_list(lis):
        res = []

        def te1(t):
            te = []
            t2 = []
            for i in t:
                if len(te) == 0:
                    te.append(i)
                else:
                    if i[1] in [t[1] for t in te]:
                        te.append(i)
                    else:
                        t2.append(i)
            res.append(te)
            if len(t2):
                te1(t2)
            return res

        return te1(lis)

    def warning_queue(self):
        """报警队列"""
        redis_list = redis_queue.warning_bpop_queue("_warning_result_", timeout=30)
        if redis_list is not None:
            logger.info("Warning result: {}".format(redis_list))
            filter_list = []
            for result in json.loads(redis_list):
                # 添加一个逻辑判断，如果该重点人员已经被删除，那么就不应该创建重点人员的抓拍记录
                monitor_instance = monitor_models.Monitor.objects.get(
                    id=Hasher.to_object_pk(result[0])
                )
                if monitor_instance.delete_at:
                    logger.info("{} is delete".format(result))
                    # 再次删除人像
                    face_discern.face_warning_detect(
                        user_id=monitor_instance.hash,
                        image=base64.b64encode(
                            requests.get(url=monitor_instance.get_head_url()).content
                        ).decode(),
                    )
                else:
                    logger.info("{} data is append filter list.".format(result))
                    filter_list.append(result)
            logger.info(filter_list)
            if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:  # 大屏推送功能
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
            for res in self.mapper_list(filter_list):
                logger.info("The same as device photo:{}".format(res))
                if len(res) > 1:
                    res = sorted(res, key=lambda x: x[2], reverse=True)
                    initial_monitor = 0
                    initial_area = 0
                    for i in res:
                        query = monitor_models.Monitor.objects.get(
                            id=Hasher.to_object_pk(i[0])
                        )
                        if query.area:
                            if initial_area == 0:
                                try:
                                    instance = (
                                        monitor_models.MonitorDiscover.objects.create(
                                            target_id=Hasher.to_object_pk(i[0]),
                                            record_id=Hasher.to_object_pk(i[1]),
                                            similarity=i[-1],
                                        )
                                    )
                                    logger.info(
                                        "Area Warning add success: {}".format(i)
                                    )
                                    initial_area += 1
                                except ValueError as e:
                                    logger.error("result parser error:{}".format(e))
                        else:
                            if initial_monitor == 0:
                                try:
                                    instance = (
                                        monitor_models.MonitorDiscover.objects.create(
                                            target_id=Hasher.to_object_pk(i[0]),
                                            record_id=Hasher.to_object_pk(i[1]),
                                            similarity=i[-1],
                                        )
                                    )
                                    if (
                                        settings.BIG_SCREEN and settings.PUSH_ROLL_CALL
                                    ):  # 是否启用大屏
                                        # 如果该instance在最近5分钟之后没有值
                                        monitor_obj = monitor_models.MonitorDiscover.objects.filter(
                                            record__take_photo_time__range=(
                                                start_time,
                                                end_time,
                                            ),
                                            target_id=instance.target_id,
                                        )
                                        if not monitor_obj.exclude(
                                            id=instance.id
                                        ).exists():
                                            # 重点人员预警ws推送
                                            if monitor_obj.exists():
                                                print(instance.target.name)
                                                consumer.send_message(
                                                    message_type="record",
                                                    message=monitor_serializers.MonitorDiscoverSerializer(
                                                        instance
                                                    ).data,
                                                )
                                    logger.info(
                                        "Monitor Warning add success: {}".format(i)
                                    )
                                    initial_monitor += 1
                                except ValueError as e:
                                    logger.error("result parser error:{}".format(e))
                else:
                    try:
                        instance = monitor_models.MonitorDiscover.objects.create(
                            target_id=Hasher.to_object_pk(res[0][0]),
                            record_id=Hasher.to_object_pk(res[0][1]),
                            similarity=res[0][-1],
                        )
                        if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:  # 是否启用大屏
                            # 如果该instance在最近5分钟之后没有值
                            monitor_obj = monitor_models.MonitorDiscover.objects.filter(
                                record__take_photo_time__range=(start_time, end_time),
                                target_id=instance.target_id,
                            )
                            if not monitor_obj.exclude(id=instance.id).exists():
                                # 重点人员预警ws推送
                                if monitor_obj.exists():
                                    print(instance.target.name)
                                    consumer.send_message(
                                        message_type="record",
                                        message=monitor_serializers.MonitorDiscoverSerializer(
                                            instance
                                        ).data,
                                    )
                        logger.info("Warning add success: {}".format(res[0]))
                    except ValueError as e:
                        logger.error("result parser error:{}".format(e))
        else:
            logger.info("Get Info from redis empty")
