import requests
import base64
import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status

from archives import models
from archives import serializers
from public.views import HashRetrieveViewSetMixin
from utils.face_discern import face_discern


# Create your views here.


class ArchivesGroupViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """档案分组ViewSet"""

    queryset = models.ArchivesGroup.objects.filter(delete_at__isnull=True).order_by(
        "create_at"
    )
    serializer_class = serializers.ArchivesGroupSerializer

    def filter_queryset(self, queryset):
        name = self.request.query_params.get("name", None)
        if name:
            queryset = queryset.filter(name__contains=name)
        return super(ArchivesGroupViewSet, self).filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
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

    @action(methods=["GET"], detail=False, url_path="count")
    def count(self, request, *args, **kwargs):
        """档案统计"""
        archives_group_total = models.ArchivesGroup.objects.count()
        archives_personnel_total = models.Personnel.objects.count()
        data = {
            "archives_group_total": archives_group_total,
            "archives_personnel_total": archives_personnel_total,
        }
        return Response(data)


class PersonnelViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """人员ViewSet"""

    queryset = models.Personnel.objects.filter(delete_at__isnull=True).order_by(
        "-create_at"
    )
    serializer_class = serializers.PersonnelSerializer

    def filter_queryset(self, queryset):
        archives_group = self.request.query_params.get("archives_group", None)
        if archives_group:
            queryset = queryset.filter(
                archives_group_id=self.hash_to_pk(archives_group)
            )
        return super(PersonnelViewSet, self).filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
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

    def create(self, request, *args, **kwargs):
        """新增档案人员"""
        try:
            request.data._mutable = True
        except Exception as e:
            raise exceptions.ParseError("档案人员新增失败.")
        finally:
            for item in list(request.data):  # 防止序列化校验异常
                if not request.data[item] and request.data[item] != 0:
                    request.data.pop(item)
        request_data = request.data
        request_data["archives_group"] = self.hash_to_pk(request_data["archives_group"])
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 人脸注册阶段
        try:
            result = face_discern.face_add(
                image=base64.b64encode(
                    requests.get(url=instance.get_head_url()).content
                ).decode(),
                user_id=instance.hash,
            )
            if result.get("error") == -1:
                instance.set_delete()
                raise exceptions.ParseError("人脸注册失败.")
        except Exception as e:
            instance.set_delete()
            raise exceptions.ParseError("人脸注册失败.")
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()

    def perform_destroy(self, instance):
        """人员软删除"""
        try:
            result = face_discern.face_del(user_id=instance.hash)
            if result.get("error") == -1:
                raise exceptions.ParseError("人脸删除失败.")
        except Exception as e:
            raise exceptions.ParseError("人脸删除失败.")
        else:
            instance.set_delete()

    @action(methods=["POST"], detail=False, url_path="search-identity")
    def search_identity(self, request):
        """以图搜身份"""
        photo = request.POST.get("photo")
        image = base64.b64encode(requests.get(url=photo).content).decode()
        face_id_list = face_discern.face_search(image=image)
        check_id_list = [face[0] for face in face_id_list]
        check_similarity_list = [face[1] for face in face_id_list]
        query_list = list(self.queryset.in_bulk(check_id_list).values())
        query_list.sort(key=lambda x: x.id)
        if check_similarity_list is not None:
            for query in query_list:
                query.similarity = check_similarity_list[query_list.index(query)]
            query_list.sort(key=lambda x: x.similarity, reverse=True)

        serializer = self.get_serializer(query_list, many=True)
        return Response(serializer.data)


class AccessDiscoverViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """门禁通行ViewSet"""

    queryset = models.AccessDiscover.objects.select_related(
        "target", "record"
    ).order_by("-create_at")
    serializer_class = serializers.AccessDiscoverSerializer

    def filter_queryset(self, queryset):
        target = self.request.query_params.get("target", None)
        start_time = self.request.query_params.get("start_time", None)
        end_time = self.request.query_params.get("end_time", None)
        if target:
            queryset = queryset.filter(target_id=self.hash_to_pk(target))
        if start_time and end_time:
            start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M%S")
            end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M%S")
            queryset = queryset.filter(create_at__range=(start_time, end_time))
        return super(AccessDiscoverViewSet, self).filter_queryset(queryset)
