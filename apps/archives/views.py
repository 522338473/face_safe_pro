from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.archives import models
from apps.archives import serializers
from apps.public.views import HashRetrieveViewSetMixin


# Create your views here.


class ArchivesGroupViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """档案分组ViewSet"""
    queryset = models.ArchivesGroup.objects.filter(delete_at__isnull=True).order_by('create_at')
    serializer_class = serializers.ArchivesGroupSerializer

    def filter_queryset(self, queryset):
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__contains=name)
        return super(ArchivesGroupViewSet, self).filter_queryset(queryset)

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

    @action(methods=['GET'], detail=False, url_path='count')
    def count(self, request, *args, **kwargs):
        """档案统计"""
        archives_group_total = models.ArchivesGroup.objects.count()
        archives_personnel_total = models.Personnel.objects.count()
        data = {
            'archives_group_total': archives_group_total,
            'archives_personnel_total': archives_personnel_total
        }
        return Response(data)


class PersonnelViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """人员ViewSet"""
    queryset = models.Personnel.objects.filter(delete_at__isnull=True).order_by('-create_at')
    serializer_class = serializers.PersonnelSerializer

    def filter_queryset(self, queryset):
        archives_group = self.request.query_params.get('archives_group', None)
        if archives_group:
            queryset = queryset.filter(archives_group_id=self.hash_to_pk(archives_group))
        return super(PersonnelViewSet, self).filter_queryset(queryset)

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
