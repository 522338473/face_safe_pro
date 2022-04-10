# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: constant.py
@time: 2022/3/5 17:11
"""

GENDER = (
    (1, '男'),
    (2, '女'),
    (3, '未知')
)

TYPES = (
    (1, '身份证'),
    (2, '护照'),
    (3, '港澳居民往来内地通行证'),
    (4, '其他')
)

SOURCE = (
    (0, '总控平台'),
    (1, '子平台')
)

CONTROL = (
    (0, '总控平台'),
    (1, '子平台'),
    (2, '总控平台， 子平台'),
)

IS_ACCESS = (
    (0, '否'),
    (1, '是')
)

STATUS_CHOICE = (
    (0, '离线'),
    (1, '在线')
)

DEVICE_TYPE = (
    (0, '普通相机'),
    (1, '人脸相机'),
    (2, '门禁设备'),
    (3, '无感通行')
)

PERSON_TYPES = (
    (0, '预警人员'),
    (1, '重点人员')
)

VEHICLE_TYPES = (
    (0, '普通车辆'),
    (1, '重点车辆')
)

# fast-dfs 文件路径前缀|适配域名
FILE_PATH_PREFIX = 'fast_dfs'

# 回放视频详情类型|视频弹出框
VIDEO_PLAY_TYPE = {
    'DEVICE_PHOTO_VIDEO_PLAY': 0,  # 设备人脸回放视频
    'DEVICE_VEHICLE_VIDEO_PLAY': 1,  # 设备车辆回放视频
    'ACCESS_DISCOVER_VIDEO_PLAY': 2,  # 门禁通行回放视频
    'MONITOR_VEHICLE_VIDEO_PLAY': 3,  # 重点车辆报警回放视频
    'MONITOR_DISCOVER_VIDEO_PLAY': 4  # 重点人员报警回放视频
}

# 抓拍详情类型|详情弹出框
DETAIL_TYPE = {
    'DEVICE_PHOTO_DETAIL': 0,  # 设备人脸抓拍详情
    'DEVICE_VEHICLE_DETAIL': 1,  # 设备车辆抓拍详情
    'ACCESS_DISCOVER_DETAIL': 2,  # 门禁通行详情
    'MONITOR_VEHICLE_DETAIL': 3,  # 重点车辆报警详情
    'MONITOR_DISCOVER_DETAIL': 4,  # 重点人员报警详情
}
