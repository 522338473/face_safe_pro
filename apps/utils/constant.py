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
