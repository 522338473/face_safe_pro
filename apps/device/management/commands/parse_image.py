import json

import redis
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.device.models import DeviceInfo
from apps.device.mq_device import parse_mq_device_image, parse_mq_motor_image, parse_mq_vehicle_image


class Command(BaseCommand):
    help = 'Get the value from the message queue and write to queue'

    def handle(self, *args, **options):
        """启动命令运行这个方法"""
        print('in.')
        obj = RedisQueue()
        queue_name = 'redis_device_image'
        obj.pop_queue(queue_name=queue_name)


class RedisQueue:

    def __init__(self):
        self.host = settings.REDIS_SERVER_HOST
        self.port = settings.REDIS_SERVER_PORT
        self.ps = None
        self.client = None

    def connect(self):
        self.client = redis.Redis(host=self.host, port=int(self.port), db=0)

        self.ps = self.client.pubsub()

    @staticmethod
    def callback(response):
        receive = json.loads(response)

        vehIclePicTime = receive.get("vehIclePicTime")
        vehIcleType = receive.get("vehIcleType")
        vehIcleColor = receive.get("vehIcleColor")
        plateChar = receive.get("plateChar")
        panoramaB64 = receive.get("panoramaB64")
        vehicleB64 = receive.get("vehicleB64")
        plateB64 = receive.get("plateB64")
        deviceIP = receive.get("deviceIP")
        similarity = receive.get("similarity")
        archive_id = receive.get("hash_id")
        facePicTime = receive.get("facePicTime")
        faceData = receive.get("faceData")
        humanData = receive.get("humanData")
        faceB64 = receive.get("faceB64")
        humanB64 = receive.get("humanB64")
        facePanoramaB64 = receive.get("facePanoramaB64")
        if DeviceInfo.objects.filter(ip=deviceIP, delete_at__isnull=True).exists():

            if facePicTime:
                parse_mq_device_image(deviceIP=deviceIP, facePicTime=facePicTime, faceData=faceData,
                                      humanData=humanData, faceB64=faceB64, humanB64=humanB64, facePanoramaB64=facePanoramaB64, archive_id=archive_id, similarity=similarity)

            elif panoramaB64 and plateChar:
                parse_mq_vehicle_image(deviceIP=deviceIP, vehIclePicTime=vehIclePicTime, vehIcleType=vehIcleType,
                                       vehIcleColor=vehIcleColor, plateChar=plateChar,
                                       panoramaB64=panoramaB64, vehicleB64=vehicleB64, plateB64=plateB64)

            elif panoramaB64 and vehIcleType == "摩托车-非机动车":
                parse_mq_motor_image(deviceIP=deviceIP, vehIclePicTime=vehIclePicTime,
                                     vehIcleType=vehIcleType, panoramaB64=panoramaB64, vehicleB64=vehicleB64)

    def pop_queue(self, queue_name):
        """从消息队列获取数据"""
        self.connect()
        while 1:
            res = self.client.blpop(queue_name)
            self.callback(res[1])
