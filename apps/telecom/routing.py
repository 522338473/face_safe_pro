# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: routing.py
@time: 2021/11/23 下午2:06
"""

from django.urls import path

from telecom import consumer


websocket_urlpatterns = [
    path("v1/ws/telecom/roll_call/", consumer.RollCallConsumer.as_asgi()),
]
