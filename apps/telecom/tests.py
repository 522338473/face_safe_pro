from django.test import TestCase

# Create your tests here.

import requests
import datetime
import time

data = {
    "position": "678",
    "createAt": (datetime.datetime.now() - datetime.timedelta(seconds=6)).strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    "latlng": "[99, 10]",
    "channel": 2,
    "devIp": "192.168.2.120",
    "alarmType": 2,
}

# res = requests.post(url="http://192.168.2.85:8000/v1/telecom/optical/", json=data)
# print(res.status_code)
# print(res.json())
# print(datetime.datetime.strptime("2021-11-02 14:46:12", "%Y-%m-%d %H:%M:%S"))
# print(time.strptime("2021-11-02 14:46:12", "%Y-%m-%d %H:%M:%S"))
# print(time.mktime(time.strptime("2021-11-02 14:46:12", "%Y-%m-%d %H:%M:%S")))
# print(datetime.datetime.fromtimestamp(time.time()))
# time.mktime(time.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
# res = requests.post(url="http://192.168.2.85:5001/getcamera", json={"cameraip": "192.168.2.161", "timetag": time.mktime(time.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))})
# print(res.request.body)
# print(res.status_code)
# print(res.text)
# print("http://192.168.2.85:5000/getcamera".replace("5000", "5001"))


# def get_ip(position=None):
#     position_list = [
#         (0, 500, "192.168.2.247"),
#         (700, 1000, "192.168.2.248")
#     ]
#     if isinstance(position, str):
#         for item in position_list:
#             if int(position) in range(item[0], item[1]):
#                 return item[2]
#
#
# if __name__ == '__main__':
#     ip = get_ip("600")
#     if not ip:
#         raise Exception(".")
#     print(ip)
import random
from queue import Queue

start_time = time.time()

# [360, 14, -0.26727742101246454], [361, 13, 0.6103671964150552] ... 0: X轴 1: Y轴 2: 振幅
op_list = []


def get_point_list():
    r_100 = [random.random() * random.choice([-1, 1]) for _ in range(100)]
    r_200 = [0] * 100
    r_300 = [0] * 100
    r_400 = [0] * 100
    r_500 = [0] * 100
    r_600 = [0] * 100
    r_700 = [0] * 100
    r_800 = [0] * 100
    r_900 = [0] * 100
    r_1000 = [0] * 100
    r_list = [r_100, r_200, r_300, r_400, r_500, r_600, r_700, r_800, r_900, r_1000]
    random.shuffle(r_list)
    point_list = []
    [point_list.extend(i) for i in r_list]
    return point_list


num = 75  # 表示请求接口的次数

max_length = 75  # 表示15秒

count = set()  # 队列里的数据  表示y轴的长度 count <= max_length
for i in range(num):
    ops = get_point_list()
    for op in ops:
        if op != 0:
            op_list.append([ops.index(op), i, op])  # 筛选符合规则的点
    for j in op_list:  # 计数器
        count.add(i)
        if len(count) > max_length:
            index = count.pop()  # 需要删除的索引元素
            for op in op_list[::-1]:
                if op[1] == index:
                    op_list.remove(op)

for k, v in enumerate(op_list):
    if num <= max_length:  # 请求次数<=最大长度
        v[1] = num - v[1] - 1
    else:  # 请求次数>最大长度
        v[1] = num - v[1] - 1

print(len(op_list), op_list)
print(time.time() - start_time)

print(random.sample(list(range(100, 2000)), 978))

p_url = "http://192.168.2.85/v1/telecom/optical/push_waterfall/"

data = {
    "channel": 1,
    "createAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
    "data": random.sample(list(range(100, 2000)), 978),
}

res = requests.post(url=p_url, json=data)
print(res.status_code)
print(res.json())
