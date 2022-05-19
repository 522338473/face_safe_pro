# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: consumer.py
@time: 2021/11/23 下午2:06
"""

from channels.generic.websocket import WebsocketConsumer


class WebSocket(WebsocketConsumer):
    def connect(self):
        """收到连接"""
        return super(WebSocket, self).connect()

    def disconnect(self, code):
        """断开链接"""
        return super(WebSocket, self).disconnect(code)

    def receive(self, text_data=None, bytes_data=None):
        """收到消息"""
        self.send(text_data, bytes_data)

    def send(self, text_data=None, bytes_data=None, close=False):
        """发送消息"""
        return super(WebSocket, self).send(text_data, bytes_data, close)
