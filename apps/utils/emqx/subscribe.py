# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: subscribe.py
@time: 2022/5/7 21:30
"""

import json
import time

from paho.mqtt import client as mqtt_client


class Subscribe:
    """消息订阅者"""

    def __init__(self, client_id, host, port, keepalive=60):
        self.client_id = client_id
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.topic = None
        self.username = "admin"
        self.password = "admin"

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        """当代理响应连接请求时调用"""
        print("on_connect: ", client, rc)

    @staticmethod
    def on_disconnect(client, userdata, rc):
        """当与代理断开连接时调用"""
        print("on_disconnect: ", client, rc)

    @staticmethod
    def on_message(client, userdata, message):
        """当收到关于客户订阅的主题的消息时调用"""
        print("on_message: ", client)
        _message = json.loads(message.payload.decode())
        print(_message)
        client_id = _message.get("client_id")
        data = _message.get("data")
        # 这里执行单独业务逻辑，如果是HTTP请求，建议设置超时时间
        client.publish(
            client_id,
            payload=json.dumps({"client_id": client_id, "message": "自定义消息体返回."}),
            qos=1,
        )

    @staticmethod
    def on_publish(client, userdata, mid):
        """当使用使用publish()发送的消息已经传输到代理时被调用"""
        print("on_publish: ", client, userdata, mid)

    @staticmethod
    def on_subscribe(client, userdata, mid, granted_qos):
        """当代理响应订阅请求时被调用"""
        print("on_subscribe: ", client)

    @staticmethod
    def on_unsubscribe(client, userdata, mid):
        """当代理响应取消订阅请求时调用"""
        print("on_unsubscribe: ", client)

    @staticmethod
    def on_log(client, userdata, level, buf):
        """当客户端有日志信息时调用"""
        print("on_log: ", client)

    def connect_mqtt(self):
        """连接mqtt服务器"""
        client = mqtt_client.Client(
            self.client_id, protocol=mqtt_client.MQTTv311, transport="tcp"
        )
        client.username_pw_set(self.username, self.password)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_publish = self.on_publish
        client.on_subscribe = self.on_subscribe
        client.on_unsubscribe = self.on_unsubscribe
        # client.on_log = self.on_log
        client.connect(host=self.host, port=self.port, keepalive=self.keepalive)
        return client

    @staticmethod
    def subscribe(client, topic):
        """发布消息"""
        client.subscribe(topic, qos=1)

    def receive(self, topic):
        """主程序运行"""
        self.topic = topic
        client = self.connect_mqtt()
        self.subscribe(client, topic)
        client.loop_forever()


if __name__ == "__main__":
    _client_id = "mqtt-tcp-sub-{id}".format(id=time.time() * 100000)
    pub = Subscribe(
        client_id=_client_id, host="124.222.222.101", port=1883, keepalive=60
    )
    pub.receive(topic="TEST")
