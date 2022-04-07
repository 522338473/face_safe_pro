from rest_framework.viewsets import ModelViewSet

from apps.monitor import models
from apps.monitor import serializers
from apps.public.views import HashRetrieveViewSetMixin


# Create your views here.


class MonitorDiscoverViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """预警信息ViewSet"""
    queryset = models.MonitorDiscover.objects.select_related('target', 'record').order_by('-create_at')
    serializer_class = serializers.MonitorDiscoverSerializer
