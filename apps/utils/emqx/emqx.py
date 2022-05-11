# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: emqx.py
@time: 2022/5/7 15:18
"""

import time

from publish import Publish
from subscribe import Subscribe


class Emqx:
    def __init__(self):
        pass

    @staticmethod
    def publish():
        """
        发布消息
        data参数为自定义消息体
        """
        _client_id = "mqtt-tcp-pub-{id}".format(id=time.time() * 100000)
        data = {"client_id": _client_id, "data": {"k": "v"}}

        pub = Publish(
            client_id=_client_id, host="124.222.222.101", port=1883, keepalive=60
        )
        pub.send(topic="TEST", message=data)
        print(pub.message)

    @staticmethod
    def subscribe():
        """订阅消息"""
        _client_id = "mqtt-tcp-sub-{id}".format(id=time.time() * 100000)
        pub = Subscribe(
            client_id=_client_id, host="124.222.222.101", port=1883, keepalive=60
        )
        pub.receive(topic="TEST")


if __name__ == "__main__":
    emq = Emqx()
    emq.publish()
    # emq.subscribe()
