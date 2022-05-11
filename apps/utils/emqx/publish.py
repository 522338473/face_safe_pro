# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: publish.py
@time: 2022/5/7 21:30
"""

import json
import time

from paho.mqtt import client as mqtt_client


class Publish:
    """消息发布者"""

    message = None

    def __init__(self, client_id, host, port, keepalive=60):
        self.client_id = client_id
        self.host = host
        self.port = port
        self.keepalive = keepalive
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

    def on_message(self, client, userdata, message):
        """当收到关于客户订阅的主题的消息时调用"""
        print("on_message: ", client, message)
        _message = json.loads(message.payload.decode())
        self.message = _message
        client.disconnect()

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
    def publish(client, topic, message):
        """发布消息"""
        result = client.publish(topic, payload=json.dumps(message), qos=1)
        status = result[0]
        if status == 0:
            print(f"send {message} to {topic}")
        else:
            client.loop_stop()
            print(f"failed to send message to {topic}")

    def send(self, topic, message):
        """主程序运行"""
        client = self.connect_mqtt()
        self.publish(client=client, topic=topic, message=message)
        client.subscribe(self.client_id)
        client.loop_forever()


if __name__ == "__main__":
    _client_id = "mqtt-tcp-pub-{id}".format(id=time.time() * 100000)
    data = {"client_id": _client_id, "data": {"k": "v"}}

    pub = Publish(client_id=_client_id, host="124.222.222.101", port=1883, keepalive=60)
    pub.send(topic="TEST", message=data)
    print(pub.message)
