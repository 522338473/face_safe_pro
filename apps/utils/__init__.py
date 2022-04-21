# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: __init__.py.py
@time: 2022/3/3 17:35
"""

import socket
import struct


class Switch:
    """ip, int 互转"""

    @staticmethod
    def num2ip(num):
        """
        :param num: 待转换的数字
        :return: 返回转换后的ip地址 | int ==> ip
        """
        # 数字 ==> ip # 数字范围[0, 255^4]
        # lambda x: '.'.join([str(x/(256**i) % 256) for i in range(3, -1, -1)])
        return socket.inet_ntoa(struct.pack('I', socket.htonl(num)))

    @staticmethod
    def ip2num(ip):
        """
        :param ip: 待转换ip地址
        :return: 返回转换后的数字 | ip ==> int
        """
        # lambda x: sum([256**j*int(i) for j, i in enumerate(x.split('.')[::-1])])
        return socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])


switch = Switch()

if __name__ == '__main__':
    ip = '192.168.2.175'
    num = 3232236207
    switch = Switch()
    print(switch.num2ip(num))
    print(switch.ip2num(ip))
