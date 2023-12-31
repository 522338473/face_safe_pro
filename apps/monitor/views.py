import datetime
import base64
import requests

from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

from archives import models as archives_models
from monitor import models
from monitor import serializers
from public.views import HashRetrieveViewSetMixin
from utils.face_discern import face_discern


# Create your views here.
from telecom import consumer


class PersonnelTypeViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """重点人员分类ViewSet"""

    queryset = models.PersonnelType.objects.order_by("-create_at")
    serializer_class = serializers.PersonnelTypeSerializer


class MonitorViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """重点人员ViewSet"""

    queryset = models.Monitor.objects.select_related("personnel_types")
    serializer_class = serializers.MonitorSerializer

    def filter_queryset(self, queryset):
        personnel_types = self.request.query_params.get("personnel_types", None)
        name = self.request.query_params.get("name", None)
        start_time = self.request.query_params.get("start_time", None)
        end_time = self.request.query_params.get("end_time", None)
        if personnel_types:
            queryset = queryset.filter(
                personnel_types_id=self.hash_to_pk(personnel_types)
            )
        if name:
            queryset = queryset.filter(name__contain=name)
        if start_time and end_time:
            start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M%S")
            end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M%S")
            queryset = queryset.filter(create_at__range=(start_time, end_time))
        return super(MonitorViewSet, self).filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        """新增重点人员"""
        try:
            request.data._mutable = True
        except Exception as e:
            raise exceptions.ParseError("重点人员新增失败.")
        finally:
            for item in list(request.data):  # 防止序列化校验异常
                if not request.data[item] and request.data[item] != 0:
                    request.data.pop(item)
        request_data = request.data
        request_data["personnel_types"] = self.hash_to_pk(
            request_data["personnel_types"]
        )
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 人脸注册阶段
        try:
            result = face_discern.face_warning_add(
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
        else:
            if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:
                # 重点人员新增，ws推送
                consumer.send_message(
                    message=serializer.data, message_type="personnel_add"
                )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:
            # 重点人员修改 WS推送
            consumer.send_message(
                message=serializer.data, message_type="personnel_update"
            )

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_destroy(self, instance):
        """人员软删除"""
        try:
            result = face_discern.face_warning_detect(user_id=instance.hash)
            if result.get("error") == -1:
                raise exceptions.ParseError("人脸删除失败.")
        except Exception as e:
            raise exceptions.ParseError("人脸删除失败.")
        else:
            instance.set_delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.MonitorSerializer(instance)
        self.perform_destroy(instance)
        if settings.BIG_SCREEN and settings.PUSH_ROLL_CALL:
            # 重点人员删除，WS推送
            consumer.send_message(message=serializer.data, message_type="personnel_del")
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET"], detail=False, url_path="count")
    def count(self, request, *args, **kwargs):
        """首页预警统计"""
        start_time = datetime.datetime.strptime(
            self.request.query_params.get("start_time"), "%Y%m%d%H%M%S"
        )
        end_time = datetime.datetime.strptime(
            self.request.query_params.get("end_time"), "%Y%m%d%H%M%S"
        )
        monitor_discovery_total = models.MonitorDiscover.objects.filter(
            target__area=False, create_at__range=(start_time, end_time)
        ).count()
        vehicle_discovery_total = models.VehicleMonitorDiscover.objects.filter(
            create_at__range=(start_time, end_time)
        ).count()
        area_discovery_total = archives_models.AccessDiscover.objects.filter(
            create_at__range=(start_time, end_time)
        ).count()

        data = {
            "monitor_discovery_total": monitor_discovery_total,
            "vehicle_discovery_total": vehicle_discovery_total,
            "area_discovery_total": area_discovery_total,
        }
        return Response(data)

    @action(methods=["GET"], detail=False, url_path="un_check_count")
    def un_check_count(self, request, *args, **kwargs):
        """首页预警统计"""
        monitor_discovery_total = models.MonitorDiscover.objects.filter(
            target__area=False, checked=False
        ).count()
        vehicle_discovery_total = models.VehicleMonitorDiscover.objects.filter(
            checked=False
        ).count()
        area_discovery_total = archives_models.AccessDiscover.objects.filter(
            checked=False
        ).count()

        data = {
            "monitor_discovery_total": monitor_discovery_total,
            "vehicle_discovery_total": vehicle_discovery_total,
            "area_discovery_total": area_discovery_total,
        }
        return Response(data)


class MonitorDiscoverViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """预警信息ViewSet"""

    queryset = models.MonitorDiscover.objects.select_related(
        "target", "record"
    ).order_by("-create_at")
    serializer_class = serializers.MonitorDiscoverSerializer

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
        return super(MonitorDiscoverViewSet, self).filter_queryset(queryset)


class ArchivesLibraryViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """关注人员人像库ViewSet"""

    queryset = models.ArchivesLibrary.objects.order_by("-create_at")
    serializer_class = serializers.ArchivesLibrarySerializer


class ArchivesPeopleViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """关注人员ViewSet"""

    queryset = models.ArchivesPersonnel.objects.select_related("library").order_by(
        "-create_at"
    )
    serializer_class = serializers.ArchivesPeopleSerializer

    def filter_queryset(self, queryset):
        library = self.request.query_params.get("library", None)
        if library:
            queryset = queryset.filter(library_id=self.hash_to_pk(library))
        return super(ArchivesPeopleViewSet, self).filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        """新增关注人员"""
        try:
            request.data._mutable = True
        except Exception as e:
            raise exceptions.ParseError("关注人员新增失败.")
        finally:
            for item in list(request.data):  # 防止序列化校验异常
                if not request.data[item] and request.data[item] != 0:
                    request.data.pop(item)
        request_data = request.data
        request_data["library"] = self.hash_to_pk(request_data["library"])
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 人脸注册阶段
        try:
            result = face_discern.face_focus_add(
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
            result = face_discern.face_focus_del(user_id=instance.hash)
            if result.get("error") == -1:
                raise exceptions.ParseError("人脸删除失败.")
        except Exception as e:
            raise exceptions.ParseError("人脸删除失败.")
        else:
            instance.set_delete()


class PhotoClusterViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """轨迹档案ViewSet"""

    queryset = models.PhotoCluster.objects.select_related("archives_personnel")
    serializer_class = serializers.PhotoClusterSerializer

    def filter_queryset(self, queryset):
        archives_personnel = self.request.query_params.get("archives_personnel", None)
        if archives_personnel:
            queryset = queryset.filter(
                archives_personnel_id=self.hash_to_pk(archives_personnel)
            )
        start_time = self.request.query_params.get("start_time", None)
        end_time = self.request.query_params.get("end_time", None)
        if start_time and end_time:
            start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M%S")
            end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M%S")
            queryset = queryset.filter(
                device_take_photo_time__range=(start_time, end_time)
            )
        return super(PhotoClusterViewSet, self).filter_queryset(queryset)


class VehicleMonitorViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """重点车辆ViewSet"""

    queryset = models.VehicleMonitor.objects.order_by("-create_at")
    serializer_class = serializers.VehicleMonitorSerializer


class VehicleMonitorDiscoverViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """重点车辆预警ViewSet"""

    queryset = models.VehicleMonitorDiscover.objects.select_related(
        "target", "record"
    ).order_by("-create_at")
    serializer_class = serializers.VehicleMonitorDiscoverSerializer

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
        return super(VehicleMonitorDiscoverViewSet, self).filter_queryset(queryset)


class RestrictedAreaViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """门禁列表ViewSet"""

    queryset = models.RestrictedArea.objects.order_by("-create_at")
    serializer_class = serializers.RestrictedAreaSerializer

    def filter_queryset(self, queryset):
        name = self.request.query_params.get("name", None)
        if name:
            queryset = queryset.filter(name__contains=name)
        return super(RestrictedAreaViewSet, self).filter_queryset(queryset)


class AreaMonitorPersonnelViewSet(HashRetrieveViewSetMixin, ModelViewSet):
    """门禁人员名单ViewSet"""

    queryset = models.AreaMonitorPersonnel.objects.select_related(
        "personnel", "area"
    ).order_by("-create_at")
    serializer_class = serializers.AreaMonitorPersonnelSerializer

    def filter_queryset(self, queryset):
        area = self.request.query_params.get("area", None)
        if area:
            queryset = queryset.filter(area_id=self.hash_to_pk(area))
        start_time = self.request.query_params.get("start_time", None)
        end_time = self.request.query_params.get("end_time", None)
        if start_time and end_time:
            start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M%S")
            end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M%S")
            queryset = queryset.filter(create_at__range=(start_time, end_time))
        return super(AreaMonitorPersonnelViewSet, self).filter_queryset(queryset)
