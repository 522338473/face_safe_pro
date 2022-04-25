# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: tasks.py
@time: 2022/4/21 15:34
"""

import time
import datetime

from celery import shared_task

from apps.device import models as device_models
from apps.monitor import models as monitor_models
from apps.utils.face_discern import face_discern


@shared_task
def photo_cluster():
    start_time = time.time()
    before_date = (datetime.datetime.now() - datetime.timedelta(days=1))
    queryset = monitor_models.ArchivesPersonnel.objects.filter(delete_at__isnull=True)
    for query in queryset:
        results = face_discern.face_focus_trace(
            user_id=query.hash, date=before_date.strftime('%Y%m%d')
        )
        if results is not None:
            check_id_list = [result[0] for result in results]
            check_similarity_list = [result[1] for result in results]
            query_list = list(device_models.DevicePhoto.objects.filter(create_at__gt=before_date).in_bulk(check_id_list).values())  # 对未归类的数据进行归类处理
            for item in query_list:
                try:
                    monitor_models.PhotoCluster.objects.create(
                        archives_personnel=query,
                        device_name=item.device.name,
                        device_address=item.device.address,
                        device_geo=item.device.geo,
                        device_ip=item.device.ip,
                        device_channel=item.device.channel,
                        device_take_photo_time=item.take_photo_time,
                        device_head_path=item.head_path,
                        device_back_path=item.back_path,
                        device_body_path=item.body_path,
                        device_face_data=item.face_data,
                        device_human_data=item.human_data,
                        similarity=check_similarity_list[query_list.index(item)]
                    )
                except Exception as e:
                    pass
        else:
            pass
