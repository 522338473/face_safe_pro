import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.archives import models as archives_models
from apps.monitor import models
from apps.monitor import serializers
from apps.public.views import HashRetrieveViewSetMixin


# Create your views here.


class MonitorViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """重点人员ViewSet"""
    queryset = models.Monitor.objects.all()
    serializer_class = serializers.MonitorSerializer

    @action(methods=['GET'], detail=False, url_path='count')
    def count(self, request, *args, **kwargs):
        """首页预警统计"""
        start_time = datetime.datetime.strptime(self.request.query_params.get('start_time'), '%Y%m%d%H%M%S')
        end_time = datetime.datetime.strptime(self.request.query_params.get('end_time'), '%Y%m%d%H%M%S')
        monitor_discovery_total = models.MonitorDiscover.objects.filter(target__area=False, create_at__range=(start_time, end_time)).count()
        vehicle_discovery_total = models.VehicleMonitorDiscover.objects.filter(create_at__range=(start_time, end_time)).count()
        area_discovery_total = archives_models.AccessDiscover.objects.filter(create_at__range=(start_time, end_time)).count()

        data = {
            'monitor_discovery_total': monitor_discovery_total,
            'vehicle_discovery_total': vehicle_discovery_total,
            'area_discovery_total': area_discovery_total
        }
        return Response(data)

    @action(methods=['GET'], detail=False, url_path='un_check_count')
    def un_check_count(self, request, *args, **kwargs):
        """首页预警统计"""
        monitor_discovery_total = models.MonitorDiscover.objects.filter(target__area=False, checked=False).count()
        vehicle_discovery_total = models.VehicleMonitorDiscover.objects.filter(checked=False).count()
        area_discovery_total = archives_models.AccessDiscover.objects.filter(checked=False).count()

        data = {
            'monitor_discovery_total': monitor_discovery_total,
            'vehicle_discovery_total': vehicle_discovery_total,
            'area_discovery_total': area_discovery_total
        }
        return Response(data)


class MonitorDiscoverViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """预警信息ViewSet"""
    queryset = models.MonitorDiscover.objects.select_related('target', 'record').order_by('-create_at')
    serializer_class = serializers.MonitorDiscoverSerializer


class PhotoClusterViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """轨迹档案ViewSet"""
    queryset = models.PhotoCluster.objects.select_related('archives_personnel')
    serializer_class = 1
