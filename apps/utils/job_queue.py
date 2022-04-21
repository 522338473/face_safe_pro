import json
import pika
import redis

from django_redis import get_redis_connection
from django.core.cache import cache
from django.conf import settings


class RedisQueue:
    def __init__(self):
        self.queue_name = 'default'
        self.client = self.connect()
        self.redis_client = self.connect_redis()

    def connect(self):
        return get_redis_connection(self.queue_name)

    @staticmethod
    def connect_redis(db=0):
        return redis.StrictRedis(settings.REDIS_SERVER_HOST, settings.REDIS_SERVER_PORT, db)

    def image_enqueue(self, image_list):
        client = self.redis_client
        key = '_device_image'
        client.rpush(key, json.dumps(image_list))

    def device_enqueue(self, device_info):
        client = self.redis_client
        key = '_video_db_'
        client.rpush(key, json.dumps(device_info))

    def photo_enqueue(self, photo_list):
        client = self.redis_client
        key = '_photo_image'
        client.rpush(key, json.dumps(photo_list))

    def enqueue(self, key, message):
        """
        :param key: redis_key
        :param message:
        :return:
        """
        client = self.redis_client
        client.rpush(key, json.dumps(message))

    def bl_pop_queue(self, queue_name, timeout=0):
        ret = self.redis_client.blpop(queue_name, timeout=timeout)
        try:
            return ret[1].decode()
        except TypeError:
            return None

    def warning_bpop_queue(self, queue_name, timeout=0):
        """出队列阻塞，通过timeout控制阻塞时间，timeout=0表示一直等待；key:_warning_image"""
        ret = self.redis_client.blpop(queue_name, timeout=timeout)
        try:
            return ret[1].decode()
        except TypeError:
            return None

    def photo_bpop_queue(self, queue_name, timeout=0):
        """出队列阻塞，通过timeout控制阻塞时间，timeout=0表示一直等待；key:_warning_image"""
        ret = self.redis_client.blpop(queue_name, timeout=timeout)
        try:
            return ret[1].decode()
        except TypeError:
            return None

    def redis_set_cache(self, redis_name, redis_value, ex=30):
        """设置缓存"""
        client = self.redis_client
        client.set(name=redis_name, value=redis_value, ex=ex)

    def redis_get_cache(self, redis_name):
        """读取缓存"""
        client = self.redis_client
        return client.get(redis_name)


class RabbitQueue:
    def __init__(self):
        self.channel = None

    def connect(self):
        credit = pika.PlainCredentials(username=settings.RABBITMQ_USERNAME, password=settings.RABBITMQ_PASSWORD)
        self.channel = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credit)).channel()

    def image_enqueue(self, image_list):
        """推送抓拍数据"""
        self.connect()
        channel = self.channel
        key = '_device_image'
        channel.queue_declare(queue=key, durable=True)  # 队列持久化
        channel.basic_publish(
            exchange='',
            routing_key=key,
            body=json.dumps(image_list, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2,  # 消息持久化
            )
        )

        channel.close()

    def photo_enqueue(self, photo_list):
        """推送注册信息"""
        self.connect()
        channel = self.channel
        key = '_photo_image'
        channel.queue_declare(queue=key, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=key,
            body=json.dumps(photo_list),
            properties=pika.BasicProperties(
                delivery_mode=2,  # 消息持久化
            )
        )

        channel.close()

    def warning_bpop_queue(self, queue_name, timeout=0):
        """从消息队列获取数据"""
        self.connect()
        channel = self.channel
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(on_message_callback=self.callback, queue=queue_name, auto_ack=False)
        channel.start_consuming()

    def callback(self, message):
        """回调函数"""
        pass


class RedisCache:
    """缓存人脸识别返回数据"""

    @staticmethod
    def redis_set_cache(redis_name, result_list, timeout=3600):
        """设置缓存"""
        return cache.set(redis_name, result_list, timeout=timeout)

    @staticmethod
    def redis_get_cache(redis_name):
        """获取缓存"""
        return cache.get(redis_name)


redis_queue = RedisQueue()
redis_cache = RedisCache()
