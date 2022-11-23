# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: routing.py
@time: 2021/11/23 下午2:06
"""

from django.urls import path

from public import consumer


websocket_urlpatterns = [path("v1/ws/consumer/", consumer.WebSocket.as_asgi())]
