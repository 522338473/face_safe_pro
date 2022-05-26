# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: consumer.py
@time: 2021/11/23 下午2:06
"""
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class RollCallConsumer(AsyncJsonWebsocketConsumer):
    group_name = "face_safe_pro"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        await self.send(text_data)

    async def send(self, text_data=None, bytes_data=None, close=False):
        await super(RollCallConsumer, self).send(text_data, bytes_data, close)

    async def push_messages(self, message):
        message_type = message["message_type"]
        message = message["message"]
        data = {"message_type": message_type, "message": message}
        await self.send(json.dumps(data, ensure_ascii=False))


def send_message(group_name="face_safe_pro", message=None, message_type=None):
    """
    WS广播: 外部函数调用
    :param message_type: 消息类型
    :param group_name: 组名称
    :param message: 消息内容
    :return:
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {"type": "push.messages", "message": message, "message_type": message_type},
    )
