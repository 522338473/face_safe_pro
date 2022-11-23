import re
import base64
import datetime
import json

import redis
from django.conf import settings
from django.core.management.base import BaseCommand

from device.models import DeviceInfo, DevicePhoto, Vehicle, Motor
from archives.models import AccessDiscover
from monitor.models import VehicleMonitor, VehicleMonitorDiscover
from utils.fast_dfs import upload_image
from utils.job_queue import redis_queue
from utils.hasher import Hasher
from utils.constant import IP_PATTERN


class Command(BaseCommand):
    help = "Get the value from the message queue and write to queue"

    def handle(self, *args, **options):
        """启动命令运行这个方法"""
        print("in.")
        obj = RedisQueue()
        queue_name = "redis_device_image"
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

    def pop_queue(self, queue_name):
        """从消息队列获取数据"""
        self.connect()
        while 1:
            res = self.client.blpop(queue_name)
            self.callback(res[1])

    def callback(self, response):
        receive = json.loads(response)

        vehicle_pic_time = receive.get("vehIclePicTime")
        vehicle_type = receive.get("vehIcleType")
        vehicle_color = receive.get("vehIcleColor")
        plate_char = receive.get("plateChar")
        panorama_b64 = receive.get("panoramaB64")
        vehicle_b64 = receive.get("vehicleB64")
        plate_b64 = receive.get("plateB64")
        device_ip = receive.get("deviceIP")
        similarity = receive.get("similarity")
        archive_id = receive.get("hash_id")
        face_pic_time = receive.get("facePicTime")
        face_data = receive.get("faceData")
        human_data = receive.get("humanData")
        face_b64 = receive.get("faceB64")
        human_b64 = receive.get("humanB64")
        face_panorama_b64 = receive.get("facePanoramaB64")
        if DeviceInfo.objects.filter(ip=device_ip, delete_at__isnull=True).exists():

            if face_pic_time:
                self.parse_mq_device_image(
                    device_ip=device_ip,
                    face_pic_time=face_pic_time,
                    face_data=face_data,
                    human_data=human_data,
                    face_b64=face_b64,
                    human_b64=human_b64,
                    face_panorama_b64=face_panorama_b64,
                    archive_id=archive_id,
                    similarity=similarity,
                )

            elif panorama_b64 and plate_char:
                self.parse_mq_vehicle_image(
                    device_ip=device_ip,
                    vehicle_pic_time=vehicle_pic_time,
                    vehicle_type=vehicle_type,
                    vehicle_color=vehicle_color,
                    plate_char=plate_char,
                    panorama_b64=panorama_b64,
                    vehicle_b64=vehicle_b64,
                    plate_b64=plate_b64,
                )

            elif panorama_b64 and vehicle_type == "摩托车-非机动车":
                self.parse_mq_motor_image(
                    device_ip=device_ip,
                    vehicle_pic_time=vehicle_pic_time,
                    vehicle_type=vehicle_type,
                    panorama_b64=panorama_b64,
                    vehicle_b64=vehicle_b64,
                )

    @staticmethod
    def parse_mq_device_image(
        device_ip,
        face_pic_time,
        face_data,
        human_data,
        face_b64,
        human_b64,
        face_panorama_b64,
        archive_id=None,
        similarity=None,
    ):
        """人脸抓拍解析"""
        face_pic_time = datetime.datetime.fromtimestamp(float(face_pic_time / 1000))
        try:
            query = DeviceInfo.objects.filter(delete_at__isnull=True).get(ip=device_ip)
        except Exception as e:
            raise
        image_list = []
        face_dict = dict()
        face_dict["face_b64"] = face_b64
        face_dict["face_panorama_b64"] = face_panorama_b64
        face_dict["human_b64"] = human_b64
        path_dict = {"face_path": None, "body_path": None, "back_path": None}
        for face in face_dict:
            if face == "face_b64":
                path = upload_image(base64.b64decode(face_dict[face]))
                path_dict["face_path"] = path
            elif face == "face_panorama_b64":
                path = upload_image(base64.b64decode(face_dict[face]))
                path_dict["back_path"] = path
            else:
                path = upload_image(base64.b64decode(face_dict[face]))
                path_dict["body_path"] = path

        res = DevicePhoto.objects.create(
            device=query,
            take_photo_time=face_pic_time,
            head_path=path_dict["face_path"],
            body_path=path_dict["body_path"],
            back_path=path_dict["back_path"],
            address=query.address,
            geo=query.geo,
            human_data=json.dumps(human_data, ensure_ascii=False)
            if human_data
            else "{}",
            face_data=json.dumps(face_data, ensure_ascii=False) if face_data else "{}",
        )
        # 将人脸照片的路径丢入redis数据库
        image_list.append(
            [
                res.hash,
                re.subn(
                    pattern=IP_PATTERN,
                    repl=settings.D_REDIS_SERVER_HOST,
                    string=res.get_head_url(),
                )[0]
                if settings.DOUBLE_NETWORK
                else res.get_head_url(),
                query.hash,
            ]
        )
        redis_queue.image_enqueue(image_list)

        if archive_id:  # 通行记录
            try:
                AccessDiscover.objects.create(
                    target_id=Hasher.to_object_pk(archive_id),
                    record_id=res.id,
                    similarity=similarity,
                )
            except Exception as e:
                pass

    @staticmethod
    def parse_mq_vehicle_image(
        device_ip,
        vehicle_pic_time,
        vehicle_type,
        vehicle_color,
        plate_char,
        panorama_b64,
        vehicle_b64,
        plate_b64,
    ):
        """车辆抓拍解析"""
        vehicle_pic_time = datetime.datetime.fromtimestamp(
            float(vehicle_pic_time / 1000)
        )
        try:
            query = DeviceInfo.objects.filter(delete_at__isnull=True).get(ip=device_ip)
        except Exception as e:
            raise
        vehicle_dict = dict()
        vehicle_dict["panorama_b64"] = panorama_b64
        vehicle_dict["vehicle_b64"] = vehicle_b64
        vehicle_dict["plate_b64"] = plate_b64
        path_dict = {"panorama_path": None, "vehicle_path": None, "plate_path": None}
        for vehicle in vehicle_dict:
            if vehicle == "panorama_b64":
                path = upload_image(base64.b64decode(vehicle_dict[vehicle]))
                path_dict["panorama_path"] = path
            elif vehicle == "vehicle_b64":
                path = upload_image(base64.b64decode(vehicle_dict[vehicle]))
                path_dict["vehicle_path"] = path
            else:
                path = upload_image(base64.b64decode(vehicle_dict[vehicle]))
                path_dict["plate_path"] = path

        vehicle_id = Vehicle.objects.create(
            take_photo_time=vehicle_pic_time,
            types=vehicle_type,
            color=vehicle_color,
            plate=plate_char,
            address=query.address,
            geo=query.geo,
            plate_path=path_dict["plate_path"],
            vehicle_path=path_dict["vehicle_path"],
            panorama_path=path_dict["panorama_path"],
            device_id=query.id,
        )
        if (
            VehicleMonitor.objects.filter(
                delete_at__isnull=True, plate=plate_char
            ).exists()
            and vehicle_id
        ):
            instance = VehicleMonitorDiscover.objects.create(
                target_id=VehicleMonitor.objects.filter(delete_at__isnull=True)
                .get(plate=plate_char)
                .pk,
                record_id=vehicle_id.id,
            )

    @staticmethod
    def parse_mq_motor_image(
        device_ip, vehicle_pic_time, vehicle_type, panorama_b64, vehicle_b64
    ):
        """非机动车抓拍解析"""
        vehicle_pic_time = datetime.datetime.fromtimestamp(
            float(vehicle_pic_time / 1000)
        )
        try:
            query = DeviceInfo.objects.filter(delete_at__isnull=True).get(ip=device_ip)
        except Exception as e:
            raise
        vehicle_dict = dict()
        vehicle_dict["panorama_b64"] = panorama_b64
        vehicle_dict["vehicle_b64"] = vehicle_b64
        path_dict = {
            "panorama_path": None,
            "vehicle_path": None,
        }

        for vehicle in vehicle_dict:
            if vehicle == "panoramaB64":
                path = upload_image(base64.b64decode(vehicle_dict[vehicle]))
                path_dict["panorama_path"] = path
            elif vehicle == "vehicleB64":
                path = upload_image(base64.b64decode(vehicle_dict[vehicle]))
                path_dict["vehicle_path"] = path

        Motor.objects.create(
            take_photo_time=vehicle_pic_time,
            types=vehicle_type,
            address=query.address,
            geo=query.geo,
            motor_path=path_dict["vehicle_path"],
            panorama_path=path_dict["panorama_path"],
            device_id=query.id,
        )
