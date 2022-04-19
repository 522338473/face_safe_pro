# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: serializers.py
@time: 2022/3/5 12:30
"""

from rest_framework import serializers

from apps.device import models


class DeviceInfoSerializers(serializers.ModelSerializer):
    """设备serializer管理器"""

    id = serializers.ReadOnlyField(source='hash')

    class Meta:
        model = models.DeviceInfo
        fields = ['id', 'name', 'ip', 'status', 'channel', 'address', 'geo', 'rtsp_address']


class DevicePhotoSerializers(serializers.ModelSerializer):
    """人脸抓拍serializer管理器"""

    id = serializers.ReadOnlyField(source='hash')
    take_photo_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    device = DeviceInfoSerializers()

    class Meta:
        model = models.DevicePhoto
        fields = ['id', 'device', 'take_photo_time', 'head_path', 'body_path', 'back_path', 'face_data', 'human_data', 'address', 'geo', 'create_at']
