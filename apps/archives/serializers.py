# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: serializers.py
@time: 2022/3/5 12:30
"""

from rest_framework import serializers

from archives import models
from device import serializers as device_serializer


class ArchivesGroupSerializer(serializers.ModelSerializer):
    """档案分组serializer管理器"""

    id = serializers.ReadOnlyField(source="hash")

    class Meta:
        model = models.ArchivesGroup
        fields = ["id", "name"]


class PersonnelSerializer(serializers.ModelSerializer):
    """人员serializer管理器"""

    id = serializers.ReadOnlyField(source="hash")
    # archives_group = ArchivesGroupSerializer(read_only=True)
    similarity = serializers.SerializerMethodField()

    @staticmethod
    def get_similarity(obj):
        """增加扩展字段"""
        try:
            return obj.similarity
        except Exception as e:
            return ""

    class Meta:
        model = models.Personnel
        fields = [
            "id",
            "archives_group",
            "name",
            "photo",
            "gender",
            "phone",
            "id_card",
            "address",
            "date_of_birth",
            "household_register",
            "nationality",
            "similarity",
        ]


class AccessDiscoverSerializer(serializers.ModelSerializer):
    """门禁通行serializer管理器"""

    id = serializers.ReadOnlyField(source="hash")
    target = PersonnelSerializer(read_only=True)
    record = device_serializer.DevicePhotoSerializers(read_only=True)

    class Meta:
        model = models.AccessDiscover
        fields = ["id", "target", "record"]
