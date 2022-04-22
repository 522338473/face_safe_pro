# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: tasks.py
@time: 2022/4/21 15:34
"""

import os
import time
import psutil

from django.conf import settings
from celery import shared_task


class ClearDisk4psUtil:
    """采用PSUtil模块进行磁盘清理"""

    def __init__(self):
        self.path = settings.SSD_DIR  # env配置安装路径 SSD_DIR
        self.day = settings.DEL_DAY  # 默认删除多少天以前的数据 DEL_DAY
        self.rate = settings.DEL_RATE  # 超过多少触发删除 DEL_RATE

    def get_disk_info(self):
        """获取磁盘信息"""
        total, used, free, percent = psutil.disk_usage(self.path)
        total = round(total / (1024 ** 3), 2)
        used = round(used / (1024 ** 3), 2)
        free = round(free / (1024 ** 3))

        print("磁盘总容量(G): ", total)
        print("磁盘已使用(G):", used)
        print("磁盘空闲(G):", free)
        print("磁盘使用百分比(%):", percent)
        return total, used, free, percent

    def clear_disk(self):
        """磁盘清理主程序"""
        _, _, _, percent = self.get_disk_info()
        clear_cmd = 'find %s/fastdfs/files/fast_dfs/snap/ -mtime +%d -type d -name "*" -exec rm -rf {} \\'  # 路径+天数
        while percent > self.rate:  # 使用率大于默认配置，触发清理程序
            cmd = clear_cmd % (self.path, self.day)
            os.system(cmd)  # 开启
            time.sleep(1)
            self.day -= 1
            _, _, _, percent = self.get_disk_info()
            if percent < self.rate:
                break
        else:
            pass


@shared_task
def clear_disk():
    """磁盘清理程序"""
    clear = ClearDisk4psUtil()
    clear.clear_disk()
