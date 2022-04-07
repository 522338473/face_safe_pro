import datetime

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from apps.device import models
from apps.device import serializers
from apps.public.views import HashRetrieveViewSetMixin


# Create your views here.


class DeviceInfoViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """设备信息ViewSet"""
    queryset = models.DeviceInfo.objects.filter(delete_at__isnull=True).order_by('create_at')
    serializer_class = serializers.DeviceInfoSerializers

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
        return Response({'url': 'http://192.168.2.95:8083/stream/f1ddee0d7cf3a88f42b958a4053ea566/channel/0/webrtc?uuid=f1ddee0d7cf3a88f42b958a4053ea566&channel=0%s' % device})


class DevicePhotoViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """人脸抓拍ViewSet"""
    queryset = models.DevicePhoto.objects.select_related('device').order_by('-take_photo_time')
    serializer_class = serializers.DevicePhotoSerializers

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
