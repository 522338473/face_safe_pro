# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: serializers.py
@time: 2022/3/5 12:31
"""

from rest_framework import serializers

from apps.monitor import models
from apps.device import serializers as device_serializers


class PersonnelTypeSerializer(serializers.ModelSerializer):
    """重点人员分类serializer管理器"""
    id = serializers.ReadOnlyField(source='hash')

    class Meta:
        model = models.PersonnelType
        fields = ['id', 'name']


class MonitorSerializer(serializers.ModelSerializer):
    """重点人员serializer管理器"""
    id = serializers.ReadOnlyField(source='hash')
    personnel_types = PersonnelTypeSerializer()

    class Meta:
        model = models.Monitor
        fields = ['id', 'personnel_types', 'name', 'gender', 'photo', 'phone', 'id_number']


class MonitorDiscoverSerializer(serializers.ModelSerializer):
    """预警信息serializer管理器"""

    id = serializers.ReadOnlyField(source='hash')
    record = device_serializers.DevicePhotoSerializers()
    target = MonitorSerializer()

    class Meta:
        model = models.MonitorDiscover
        depth = 2
        fields = ['id', 'target', 'record', 'checked', 'similarity']


class ArchivesLibrarySerializer(serializers.ModelSerializer):
    """人像库serializer管理器"""

    id = serializers.ReadOnlyField(source='hash')

    class Meta:
        model = models.ArchivesLibrary
        fields = ['id', 'name']


class ArchivesPeopleSerializer(serializers.ModelSerializer):
    """关注人员serializer管理器"""

    id = serializers.ReadOnlyField(source='hash')
    library = ArchivesLibrarySerializer()

    class Meta:
        model = models.ArchivesPersonnel
        depth = 2
        fields = ['id', 'library', 'name', 'phone', 'id_card']


class PhotoClusterSerializer(serializers.ModelSerializer):
    """轨迹档案serializer管理器"""

    id = serializers.ReadOnlyField(source='hash')
    archives_personnel = ArchivesPeopleSerializer()

    class Meta:
        model = models.PhotoCluster
        fields = ['id', 'archives_personnel']
