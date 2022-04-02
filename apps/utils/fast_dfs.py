# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: fast_dfs.py
@time: 2022/4/2 12:22
"""

import time
import requests

from django.conf import settings

from utils.constant import FILE_PATH_PREFIX


def upload_image(request, file_types=None):
    """
    图片上传并返回图片路径
    :param request:
    :param file_types: 文件上传类型
    :return:
    """
    if not file_types:  # 默认抓拍抓拍路径
        path = ''.join([FILE_PATH_PREFIX, '/snap/', time.strftime('%Y/%m/%d', time.localtime())])
    elif file_types == 'archives':  # 人员档案路径
        path = ''.join([FILE_PATH_PREFIX, '/archives/'])
    elif file_types == 'monitor':  # 重点人员路径
        path = ''.join([FILE_PATH_PREFIX, '/monitor/'])
    elif file_types == 'personnel':  # 关注人员路径
        path = ''.join([FILE_PATH_PREFIX, '/personnel/'])
    else:
        path = ''.join([FILE_PATH_PREFIX, '/other/'])

    files = {'file': request.FILES.get('file')}

    options = {
        'output': 'json',
        'path': path,
        'scene': ''
    }

    try:
        res = requests.post(url=''.join([settings.FAST_DFS_HOST, '/upload']), data=options, files=files).json()
        if int(res.get('size')) < 1000:
            raise
        return res['path']
    except Exception as e:
        raise
