from rest_framework import serializers

from apps.telecom import models


class OpticalFiberAlarmSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source="hash")

    class Meta:
        model = models.OpticalFiberAlarm
        fields = [
            "id",
            "createAt",
            "position",
            "geo",
            "channel",
            "devIp",
            "alarmType",
            "alarm_detail",
        ]


class AlgorithmAlarmSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source="hash")
    take_time = serializers.DateTimeField(
        source="take_photo_time", format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    dev_address = serializers.ReadOnlyField(source="device.address")
    alarm_type = serializers.ReadOnlyField(source="optical.alarmType")
    back_url = serializers.ReadOnlyField(source="get_back_url")
    channel_id = serializers.ReadOnlyField(source="device.channel")
    alarm_detail = serializers.ReadOnlyField(source="optical.alarm_detail")
    device_id = serializers.ReadOnlyField(source="device.hash")
    info = serializers.ReadOnlyField(source="detail")

    class Meta:
        model = models.AlgorithmAlarm
        fields = [
            "id",
            "take_time",
            "dev_address",
            "alarm_type",
            "back_url",
            "channel_id",
            "alarm_detail",
            "device_id",
            "info",
        ]


class RollCallHistorySerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source="hash")
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.RollCallHistory
        fields = [
            "id",
            "start_time",
            "end_time",
            "total_person",
            "attendance_person",
            "rate_of_attendance",
            "personnel_types",
            "person_list",
            "person_list_record",
        ]
