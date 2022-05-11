# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: record.py
@time: 2022/3/18 11:25
"""

import time
import datetime
import requests

map_data = [
    {
        "address": "广东省深圳市南山区桃源街道中爱花园",  # 坐标值(地址)
        "geo": "113.942267,22.581026",  # 坐标(经纬度)
        "create_at": "2022-04-14 00:02:02",  # 坐标创建时间|为空直接显示点坐标。有值根据时间排序箭头标注
    }
]

params = {"start_time": "20220407000000", "end_time": "20220408000000"}

res = requests.get(
    "http://192.168.2.9:9999/v1/device/photo/snap_count/?format=json", params
)
results = res.json()
dates = results.get("dates")
people_list = results.get("people_count")
vehicle_list = results.get("vehicle_count")

print("起止时间为: ", dates)
print("人脸统计: ", people_list)
print("车辆统计: ", vehicle_list)

print("*" * 100)
start_time = time.time()
start_date = datetime.datetime.strptime(dates["start_date"], "%Y%m%d%H%M%S")
end_date = datetime.datetime.strptime(dates["end_date"], "%Y%m%d%H%M%S")
days = datetime.timedelta(days=1)

if end_date - start_date <= days:
    people_hour_list = [{"date": "".join([str(i), "点"]), "count": 0} for i in range(24)]
    vehicle_hour_list = [
        {"date": "".join([str(i), "点"]), "count": 0} for i in range(24)
    ]
    for i in people_list:
        people_hour_list[int(i.get("date").split(":")[1])]["count"] = i.get("count")
    for i in vehicle_list:
        vehicle_hour_list[int(i.get("date").split(":")[1])]["count"] = i.get("count")
else:
    dlt_day = (end_date - start_date).days + 1
    people_hour_list = [
        {
            "date": (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"),
            "count": 0,
        }
        for i in range(dlt_day)
    ]
    vehicle_hour_list = [
        {
            "date": (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"),
            "count": 0,
        }
        for i in range(dlt_day)
    ]
    for i, v in enumerate(people_hour_list):
        for j in people_list:
            if v.get("date") == j.get("date"):
                people_hour_list[i]["count"] = j.get("count")
                break
    for i, v in enumerate(vehicle_hour_list):
        for j in vehicle_list:
            if v.get("date") == j.get("date"):
                vehicle_hour_list[i]["count"] = j.get("count")
                break

print(people_hour_list)
print(vehicle_hour_list)

print("time consume: ", time.time() - start_time)
