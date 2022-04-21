import datetime
import logging
import base64
import json
import re

from django.conf import settings

from apps.archives import models
from apps.device.models import DeviceInfo, Motor
from apps.device.models import DevicePhoto
from apps.device.models import Vehicle
from apps.monitor.models import VehicleMonitor, VehicleMonitorDiscover
from apps.utils.fast_dfs import upload_image
from apps.utils.hasher import Hasher
from apps.utils.job_queue import redis_queue
from apps.utils.constant import IP_PATTERN


def parse_mq_device_image(deviceIP, facePicTime, faceData, humanData, faceB64, humanB64, facePanoramaB64, archive_id=None, similarity=None):
    print('开始解析人脸数据')
    facePicTime = datetime.datetime.fromtimestamp(float(facePicTime / 1000))

    try:
        query = DeviceInfo.objects.filter(delete_at__isnull=True).get(ip=deviceIP)
    except Exception as e:
        raise

    image_list = []
    face_list = {}
    face_list['faceB64'] = faceB64
    face_list['panoramaB64'] = facePanoramaB64
    face_list['humanB64'] = humanB64
    path_dict = {
        'face_path': None,
        'body_path': None,
        'back_path': None
    }
    for face in face_list:
        if face == 'faceB64':
            path = upload_image(base64.b64decode(face_list[face]), file_types=None)
            path_dict['face_path'] = path
        elif face == 'panoramaB64':
            path = upload_image(base64.b64decode(face_list[face]), file_types=None)
            path_dict['back_path'] = path
        else:
            path = upload_image(base64.b64decode(face_list[face]), file_types=None)
            path_dict['body_path'] = path

    # 抓拍信息保存入pg数据库
    res = DevicePhoto.objects.create(
        device=query, take_photo_time=facePicTime,
        head_path=path_dict['face_path'], body_path=path_dict['body_path'], back_path=path_dict['back_path'],
        address=query.address, geo=query.geo,
        human_data=json.dumps(humanData, ensure_ascii=False) if humanData else "{}", face_data=json.dumps(faceData, ensure_ascii=False) if faceData else "{}"
    )
    # 将人脸照片的路径丢入redis数据库
    image_list.append([
        res.hash,
        re.subn(pattern=IP_PATTERN, repl=settings.D_REDIS_SERVER_HOST, string=res.get_head_url())[0] if settings.DOUBLE_NETWORK else res.get_head_url(),
        query.hash
    ])
    redis_queue.image_enqueue(image_list)

    if archive_id:  # 归档预警
        try:
            models.AccessDiscover.objects.create(target_id=Hasher.to_object_pk(archive_id), record_id=res.id, similarity=similarity)
        except Exception as e:
            logging.info("access alarm failed: {}".format(e))


def parse_mq_vehicle_image(deviceIP,
                           vehIclePicTime,
                           vehIcleType,
                           vehIcleColor,
                           plateChar,
                           panoramaB64,
                           vehicleB64,
                           plateB64):
    """
    :param deviceIP: 设备ip
    :param vehIclePicTime: 抓拍时间
    :param vehIcleType: 车辆类型
    :param vehIcleColor: 车辆颜色
    :param plateChar: 车牌号
    :param panoramaB64: 车辆全景照
    :param vehicleB64: 车辆抓拍照
    :param plateB64: 车牌照
    :return:
    """
    print('开始解析车辆数据')
    vehIclePicTime = datetime.datetime.fromtimestamp(float(vehIclePicTime / 1000))

    try:
        query = DeviceInfo.objects.filter(delete_at__isnull=True, status=1).get(ip=deviceIP)
    except Exception as e:
        raise

    vehicle_list = {}
    vehicle_list['panoramaB64'] = panoramaB64
    vehicle_list['vehicleB64'] = vehicleB64
    vehicle_list['plateB64'] = plateB64

    path_dict = {
        'panorama_path': None,
        'vehicle_path': None,
        'plate_path': None
    }

    for vehicle in vehicle_list:
        if vehicle == 'panoramaB64':
            path = upload_image(base64.b64decode(vehicle_list[vehicle]), file_types=None)
            path_dict['panorama_path'] = path
        elif vehicle == 'vehicleB64':
            path = upload_image(base64.b64decode(vehicle_list[vehicle]), file_types=None)
            path_dict['vehicle_path'] = path
        else:
            path = upload_image(base64.b64decode(vehicle_list[vehicle]), file_types=None)
            path_dict['plate_path'] = path

    vehicle_id = Vehicle.objects.create(
        take_photo_time=vehIclePicTime, types=vehIcleType, color=vehIcleColor, plate=plateChar,
        address=query.address, geo=query.geo,
        plate_path=path_dict['plate_path'], vehicle_path=path_dict['vehicle_path'], panorama_path=path_dict['panorama_path'], device_id=query.id
    )
    # 查询是否在重点车辆库，如果在，则添加到车辆预警库
    if VehicleMonitor.objects.filter(delete_at__isnull=True, plate=plateChar).exists() and vehicle_id:
        instance = VehicleMonitorDiscover.objects.create(target_id=VehicleMonitor.objects.filter(delete_at__isnull=True).get(plate=plateChar).pk,
                                                         record_id=vehicle_id.pk)


def parse_mq_motor_image(deviceIP, vehIclePicTime, vehIcleType, panoramaB64, vehicleB64):
    """
    :param deviceIP: 设备ip
    :param vehIclePicTime: 抓拍时间
    :param vehIcleType: 车辆类型
    :param panoramaB64: 非机动车全景照
    :param vehicleB64: 非机动车抓拍照
    :return:
    """
    print('开始解析非机动车数据')
    vehIclePicTime = datetime.datetime.fromtimestamp(float(vehIclePicTime / 1000))

    try:
        query = DeviceInfo.objects.filter(delete_at__isnull=True).get(ip=deviceIP)
    except Exception as e:
        raise

    vehicle_list = {}
    vehicle_list['panoramaB64'] = panoramaB64
    vehicle_list['vehicleB64'] = vehicleB64

    path_dict = {
        'panorama_path': None,
        'vehicle_path': None,
    }

    for vehicle in vehicle_list:
        if vehicle == 'panoramaB64':
            path = upload_image(base64.b64decode(vehicle_list[vehicle]), file_types=None)
            path_dict['panorama_path'] = path
        elif vehicle == 'vehicleB64':
            path = upload_image(base64.b64decode(vehicle_list[vehicle]), file_types=None)
            path_dict['vehicle_path'] = path

    Motor.objects.create(
        take_photo_time=vehIclePicTime, types=vehIcleType, address=query.address, geo=query.geo,
        motor_path=path_dict['vehicle_path'], panorama_path=path_dict['panorama_path'], device_id=query.id,
    )
