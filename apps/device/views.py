import datetime
import base64
import requests

from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError

from apps.device import models as device_model
from apps.archives import models as archives_model
from apps.monitor import models as monitor_model
from apps.device import serializers as device_serializer
from apps.public.views import HashRetrieveViewSetMixin
from apps.utils.face_discern import face_discern
from apps.utils.job_queue import redis_cache


# Create your views here.


class DeviceInfoViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """设备信息ViewSet"""
    queryset = device_model.DeviceInfo.objects.filter(delete_at__isnull=True).order_by('create_at')
    serializer_class = device_serializer.DeviceInfoSerializers

    def filter_queryset(self, queryset):
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__contains=name)
        return super(DeviceInfoViewSet, self).filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginate = request.query_params.get('paginate', None)
        if paginate == 'off':
            serializer = self.get_serializer(queryset, many=True)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='device_video')
    def device_video(self, request, *args, **kwargs):
        """实时监控"""
        device = self.request.query_params.get('device', None)
        if self.hash_to_pk(device) == 1:
            return Response({'url': 'http://192.168.2.84:8083/stream/6f9155485a1f85b8d2d801badf7ae09b/channel/0/webrtc?uuid=6f9155485a1f85b8d2d801badf7ae09b&channel=0&device_id=%s' % device})
        else:
            return Response({'url': 'http://192.168.2.84:8083/stream/580cfe817d3cf0ea2edc98e36e356642/channel/0/webrtc?uuid=580cfe817d3cf0ea2edc98e36e356642&channel=0&device_id=%s' % device})

    @action(methods=['GET'], detail=False, url_path='device_status')
    def device_status(self, request, *args, **kwargs):
        """摄像头状态"""
        return Response(self.get_queryset().values('status').annotate(count=Count('status')).order_by().values('status', 'count'))


class DevicePhotoViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """人脸抓拍ViewSet"""
    queryset = device_model.DevicePhoto.objects.select_related('device').order_by('-take_photo_time')
    serializer_class = device_serializer.DevicePhotoSerializers

    def filter_queryset(self, queryset):
        device = self.request.query_params.get('device', None)
        if device:
            queryset = queryset.filter(device_id=self.hash_to_pk(device))
        return super(DevicePhotoViewSet, self).filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginate = request.query_params.get('paginate', None)
        if paginate == 'off':
            serializer = self.get_serializer(queryset, many=True)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='device_snap_count')
    def device_snap_count(self, request, *args, **kwargs):
        """抓拍统计"""
        now_days_snap_total = self.get_queryset().filter(take_photo_time__gte=datetime.datetime.now().date()).count()
        all_days_snap_total = self.get_queryset().count()
        data = {
            'now_days_snap_total': now_days_snap_total,
            'all_days_snap_total': all_days_snap_total
        }
        return Response(data)

    @action(methods=['GET'], detail=False, url_path='survey')
    def survey(self, request, *args, **kwargs):
        """首页概况统计"""
        now_days_snap_total = device_model.DevicePhoto.objects.filter(take_photo_time__gte=datetime.datetime.now().date()).count()
        all_days_snap_total = device_model.DevicePhoto.objects.count()
        monitor_total = monitor_model.Monitor.objects.count()
        personnel_total = monitor_model.ArchivesPersonnel.objects.count()
        archives_total = archives_model.Personnel.objects.count()
        data = {
            'now_days_snap_total': now_days_snap_total,
            'all_days_snap_total': all_days_snap_total,
            'monitor_total': monitor_total,
            'personnel_total': personnel_total,
            'archives_total': archives_total
        }
        return Response(data)

    @action(methods=['GET'], detail=False, url_path='snap_count')
    def snap_count(self, request, *args, **kwargs):
        """首页抓拍折线图统计"""
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)
        days = datetime.timedelta(days=1)
        try:
            start_date = datetime.datetime.strptime(start_time, '%Y%m%d%H%M%S')
            end_date = datetime.datetime.strptime(end_time, '%Y%m%d%H%M%S')
        except ValueError:
            start_date = datetime.datetime.strptime(datetime.datetime.now().date().strftime('%Y%m%d%H%M%S'), '%Y%m%d%H%M%S')
            end_date = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), '%Y%m%d%H%M%S')
        count_list = {
            'dates': {
                'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
                'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%S')
            },
            'people_count': [],
            'vehicle_count': []
        }
        face_query = device_model.DevicePhoto.objects.all()
        vehicle_query = device_model.Vehicle.objects.all()

        if end_date - start_date <= days:
            face_list = face_query.filter(take_photo_time__range=(start_date, end_date)) \
                .extra(select={"take_photo_time": "to_char(take_photo_time, 'yyyy-mm-dd:HH24')"}).values('take_photo_time') \
                .annotate(count=Count('take_photo_time')).values('take_photo_time', 'count').order_by()
            car_list = vehicle_query.filter(take_photo_time__range=(start_date, end_date)) \
                .extra(select={"take_photo_time": "to_char(take_photo_time, 'yyyy-mm-dd:HH24')"}).values('take_photo_time') \
                .annotate(count=Count('take_photo_time')).values('take_photo_time', 'count').order_by()
        else:
            face_list = face_query.filter(take_photo_time__range=(start_date, end_date)) \
                .extra(select={"take_photo_time": "to_char(take_photo_time, 'yyyy-mm-dd')"}).values('take_photo_time') \
                .annotate(count=Count('take_photo_time')).values('take_photo_time', 'count').order_by()
            car_list = vehicle_query.filter(take_photo_time__range=(start_date, end_date)) \
                .extra(select={"take_photo_time": "to_char(take_photo_time, 'yyyy-mm-dd')"}).values('take_photo_time') \
                .annotate(count=Count('take_photo_time')).values('take_photo_time', 'count').order_by()

        for result in face_list:
            count_list['people_count'].append({
                'date': result['take_photo_time'],
                'count': result['count'],
            })
        for car in car_list:
            count_list['vehicle_count'].append({
                'date': car['take_photo_time'],
                'count': car['count']
            })
        return Response(count_list)

    @action(methods=['GET'], detail=False, url_path='search_image')
    def search_image(self, request, *args, **kwargs):
        """以图搜图接口"""
        photo = request.query_params.get('photo')
        time_range = int(request.query_params.get('time_range', '1'))
        sort = request.query_params.get('sort', 'timer')
        margin = int(request.query_params.get('margin', '60'))
        image = base64.b64encode(requests.get(url=photo).content).decode()
        days = datetime.timedelta(days=time_range)
        now_time = datetime.datetime.now()
        start_date = (now_time - days).strftime('%Y%m%d')
        end_date = now_time.strftime('%Y%m%d')
        results = results = redis_cache.redis_get_cache(photo)
        if not results:
            results = face_discern.search_record(image=image, start_date=start_date, end_date=end_date, margin=margin, s_margin=margin, identification=photo, search_type='searching')
            if results.get('code') == -1:
                raise ParseError('搜索服务器异常')
            results = results.get('results', [])
        results = [result for result in results if result[1] >= margin]
        check_id_list = [result[0] for result in results]
        check_similarity_list = [result[1] for result in results]  # 相似度
        query_list = list(self.filter_queryset(self.get_queryset()).in_bulk(check_id_list).values())
        query_list.sort(key=lambda x: x.id)
        if check_similarity_list is not None:
            for query in query_list:
                query.similarity = check_similarity_list[check_id_list.index(query.id)]
            query_list.sort(key=lambda x: x.take_photo_time, reverse=True)
            if sort == 'similarity':
                query_list.sort(key=lambda x: x.similarity, reverse=True)
        page = self.paginate_queryset(query_list)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(query_list, many=True)
        return Response(serializer.data)
