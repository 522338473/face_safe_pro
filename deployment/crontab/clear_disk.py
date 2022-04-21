# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: clear_disk.py
@time: 2021/4/2 下午12:32
"""

import os
import time
import psutil


class ClearDisk4os:
    """采用OS模块进行磁盘清理"""

    def __init__(self, path, day):
        self.path = path
        self.day = day
        self.rate = 0.75

    @staticmethod
    def get_disk_info(path):
        """获取磁盘挂载信息"""
        return os.statvfs(path)

    def get_disk_size(self):
        """获取磁盘总容量"""
        disk = self.get_disk_info(self.path)
        disk_size = disk.f_bsize * disk.f_blocks / (1024 ** 3)  # 1G = 1024M  1M = 1024KB 1KB = 1024bytes
        print("磁盘总容量: %s" % format(disk_size, '.2f'))
        return disk_size

    def get_disk_used(self):
        """获取磁盘已使用容量|磁盘空闲容量"""
        disk = self.get_disk_info(self.path)
        disk_size = self.get_disk_size()
        disk_used = disk.f_bsize * (disk.f_blocks - disk.f_bfree) / (1024 ** 3)
        print("磁盘已使用: %s" % format(disk_used, '.2f'))
        print("磁盘空闲: %s" % format((disk_size - disk_used), '.2f'))
        return disk_size, disk_used, disk_size - disk_used

    def get_disk_rate(self):
        """返回磁盘使用率|剩余率"""
        disk_size, disk_used, _ = self.get_disk_used()
        print("磁盘使用率: %s" % format((disk_used / disk_size), '.2f'))
        print("磁盘空闲率: %s" % format((1 - (disk_used / disk_size)), '.2f'))
        return disk_used / disk_size, 1 - (disk_used / disk_size)

    def check(self):
        """磁盘清理主进程"""
        disk_rate, _ = self.get_disk_rate()  # 磁盘使用率
        if disk_rate > self.rate:  # 磁盘使用率大于默认配置(0.75)
            clear_cmd = 'sudo find /mnt/data/fastdfs/files/snap/ -mtime +%d -type d -name "*" -exec rm -rf {} \\'
            while self.day:
                cmd = clear_cmd % self.day
                print(cmd)
                # os.system(cmd)
                time.sleep(5)
                disk_rate, _ = self.get_disk_rate()  # 磁盘使用率

                if disk_rate < self.rate:  # 使用率小于默认配置，break
                    break
                else:  # 天数-1：继续循环
                    self.day -= 1
        else:
            print('磁盘健康!')


class ClearDisk4psUtil:
    """采用PSUtil模块进行磁盘清理"""

    def __init__(self, path=None, day=180):
        self.path = path
        self.day = day
        self.rate = 20

    def get_disk_info(self):
        """获取磁盘信息"""
        total, used, free, percent = psutil.disk_usage(self.path)
        total = round(total / (1024 ** 3), 2)
        used = round(used / (1024 ** 3), 2)
        free = round(free / (1024 ** 3))

        print("磁盘总容量: ", total)
        print("磁盘已使用:", used)
        print("磁盘空闲:", free)
        print("磁盘使用百分比:", percent)
        return total, used, free, percent

    def clear_disk(self):
        """磁盘清理主程序"""
        _, _, _, percent = self.get_disk_info()
        clear_cmd = 'sudo find /mnt/data/fastdfs/files/snap/ -mtime +%d -type d -name "*" -exec rm -rf {} \\'
        while percent > self.rate:  # 使用率大于默认配置，触发清理程序
            print(percent)
            cmd = clear_cmd % self.day
            print(cmd)
            # os.system(cmd)
            time.sleep(1)
            self.day -= 1
            _, _, _, percent = self.get_disk_info()
            if percent < self.rate:
                break
        else:
            print("Disk health!")


if __name__ == '__main__':
    # device_os = ClearDisk4os(path='/Users/zhangjianping', day=7)
    # device_os.check()
    print("*" * 20)
    device_ps_util = ClearDisk4psUtil(path='/Users/zhangjianping')
    device_ps_util.clear_disk()
