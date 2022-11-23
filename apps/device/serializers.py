# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: serializers.py
@time: 2022/3/5 12:30
"""

from rest_framework import serializers

from device import models


class DeviceInfoSerializers(serializers.ModelSerializer):
    """设备serializer管理器"""

    id = serializers.ReadOnlyField(source="hash")

    class Meta:
        model = models.DeviceInfo
        fields = [
            "id",
            "name",
            "ip",
            "status",
            "channel",
            "address",
            "geo",
            "rtsp_address",
            "device_type",
        ]


class DevicePhotoSerializers(serializers.ModelSerializer):
    """人脸抓拍serializer管理器"""

    id = serializers.ReadOnlyField(source="hash")
    take_photo_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    device = DeviceInfoSerializers(read_only=True)
    similarity = serializers.SerializerMethodField()

    @staticmethod
    def get_similarity(obj):
        """增加扩展字段"""
        try:
            return obj.similarity
        except Exception as e:
            return ""

    class Meta:
        model = models.DevicePhoto
        fields = [
            "id",
            "device",
            "take_photo_time",
            "head_path",
            "body_path",
            "back_path",
            "face_data",
            "human_data",
            "address",
            "geo",
            "create_at",
            "similarity",
        ]


class VehicleSerializers(serializers.ModelSerializer):
    """机动车serializer管理器"""

    id = serializers.ReadOnlyField(source="hash")
    take_photo_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    device = DeviceInfoSerializers(read_only=True)

    class Meta:
        model = models.Vehicle
        fields = [
            "id",
            "device",
            "take_photo_time",
            "types",
            "color",
            "plate",
            "plate_path",
            "vehicle_path",
            "panorama_path",
            "address",
            "geo",
        ]


class MotorSerializers(serializers.ModelSerializer):
    """非机动车serializer管理器"""

    id = serializers.ReadOnlyField(source="hash")
    take_photo_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    device = DeviceInfoSerializers(read_only=True)

    class Meta:
        model = models.Motor
        fields = [
            "id",
            "device",
            "take_photo_time",
            "types",
            "motor_path",
            "panorama_path",
            "address",
            "geo",
        ]


class DeviceOffLineSerializers(serializers.ModelSerializer):
    """设备离线记录serializer管理器"""

    id = serializers.ReadOnlyField(source="hash")
    device = DeviceInfoSerializers(read_only=True)

    class Meta:
        model = models.DeviceOffLine
        fields = ["id", "device", "checked", "alarm_type", "photo_path"]
