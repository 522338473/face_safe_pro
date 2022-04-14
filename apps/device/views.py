import datetime

from django.db.models import Count
from django.db.models.functions import TruncDay, TruncHour
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from apps.device import models as device_model
from apps.archives import models as archives_model
from apps.monitor import models as monitor_model
from apps.device import serializers as device_serializer
from apps.public.views import HashRetrieveViewSetMixin


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
                'start_date': start_date.strftime('%Y%m%d%H%M%S'),
                'end_date': end_date.strftime('%Y%m%d%H%M%S')
            },
            'people_count': [],
            'vehicle_count': []
        }
        face_query = device_model.DevicePhoto.objects.all()
        vehicle_query = device_model.Vehicle.objects.all()

        if end_date - start_date <= days:
            format_str = '%Y-%m-%d:%H'
            face_list = face_query.filter(take_photo_time__range=(start_date, end_date)) \
                .annotate(date=TruncHour('take_photo_time')).values('date').annotate(count=Count('date')).order_by()
            vehicle_list = vehicle_query.filter(take_photo_time__range=(start_date, end_date)) \
                .annotate(date=TruncHour('take_photo_time')).values('date').annotate(count=Count('date')).order_by()
        else:
            format_str = '%Y-%m-%d'
            face_list = face_query.filter(take_photo_time__range=(start_date, end_date)) \
                .annotate(date=TruncDay('take_photo_time')).values('date').annotate(count=Count('date')).order_by()
            vehicle_list = vehicle_query.filter(take_photo_time__range=(start_date, end_date)) \
                .annotate(date=TruncDay('take_photo_time')).values('date').annotate(count=Count('date')).order_by()
        for face in face_list:
            count_list['people_count'].append({
                'date': face['date'].strftime(format_str),
                'count': face['count']
            })
        for vehicle in vehicle_list:
            count_list['vehicle_count'].append({
                'date': vehicle['date'].strftime(format_str),
                'count': vehicle['count']
            })

        return Response(count_list)
