# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: admin_view.py
@time: 2022/4/7 10:58
"""

from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.response import Response

from apps.device import models as device_models
from apps.monitor import models as monitor_models
from apps.archives import models as archives_models
from apps.device import serializers as device_serializers
from apps.public.views import ParseJsonView


# Create your views here.


class PhotoSearchView(ParseJsonView, View):
    """以图搜图模块View"""

    def get(self, request):
        """以图搜图页面返回"""
        id = request.GET.get('id')
        detail_type = request.GET.get('detail_type')
        if detail_type == '5':
            photo = monitor_models.Monitor.objects.get(id=self.hash_to_pk(id)).get_head_url()
        else:
            photo = device_models.DevicePhoto.objects.get(id=self.hash_to_pk(id)).get_head_url()
        print(detail_type, photo)
        return render(request, 'admin/popup/device/photo_search.html', locals())


class PhotoDetailView(ParseJsonView, View):
    """照片详情View"""

    def get(self, request):
        """以图搜图页面详情"""
        _id = request.GET.get('id')
        similarity = request.GET.get('similarity')
        detail_type = request.GET.get('detail_type')
        if detail_type in ['0', '5']:
            instance = device_models.DevicePhoto.objects.get(id=self.hash_to_pk(_id))
        else:
            instance = monitor_models.MonitorDiscover.objects.get(id=self.hash_to_pk(_id)).record
        head_path = instance.head_path
        body_path = instance.body_path
        back_path = instance.back_path
        device = instance.device
        address = instance.address
        human_data = instance.human_data
        face_data = instance.face_data
        take_photo_time = instance.take_photo_time
        if detail_type == '0':
            if request.GET.get('monitor_id'):
                sample_url = device_models.DevicePhoto.objects.get(id=self.hash_to_pk(request.GET.get('monitor_id'))).get_head_url()
                similarity = similarity

        elif detail_type == '4':
            monitor_ins = monitor_models.MonitorDiscover.objects.get(id=self.hash_to_pk(_id))
            similarity = monitor_ins.similarity
            sample_url = monitor_ins.target.photo
            monitor_name = monitor_ins.target.name

        elif detail_type == '5':
            monitor_id = request.GET.get('monitor_id')
            monitor_ins = monitor_models.Monitor.objects.get(id=self.hash_to_pk(monitor_id))
            similarity = similarity
            monitor_name = monitor_ins.name
            sample_url = monitor_ins.photo

        return render(request, 'admin/popup/device/photo_detail.html', locals())


class SearchImageView(ParseJsonView, View):
    """以图搜图View"""

    def get(self, request):
        """以图搜图模板返回"""
        _id = request.GET.get('id')

        if _id:
            url = archives_models.Personnel.objects.get(id=self.hash_to_pk(_id)).get_head_url()
        else:
            url = 'https://wimg.588ku.com/gif620/20/12/15/b0f831231ece9b4e422adf9bcb271c51.gif'

        return render(request, 'admin/device/other/search_image.html', locals())


class VehicleSearchView(ParseJsonView, View):
    """机动车查询View"""

    def get(self, request):
        _id = request.GET.get('id')
        return render(request, 'admin/popup/device/vehicle_search.html', locals())

    def post(self, request):
        request_data = self.parse_body(request)
        current_page = request_data.get('current_page', 1)
        page_size = request_data.get('page_size', 10)
        paginate = request_data.get('paginate')
        _id = request_data.get('id')
        _plate = device_models.Vehicle.objects.get(id=self.hash_to_pk(_id)).plate
        _photo_list = device_models.Vehicle.objects.filter(plate=_plate).order_by('-id').values('id', 'device__name', 'address', 'take_photo_time', 'plate_path')
        # _photo_list = device_models.Vehicle.objects.order_by('-id').values('id', 'device__name', 'address', 'take_photo_time', 'plate_path')
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class VehicleDetailView(ParseJsonView, View):
    """机动车详情View"""

    def get(self, request):
        _id = request.GET.get('id')
        instance = device_models.Vehicle.objects.get(id=self.hash_to_pk(_id))
        return render(request, 'admin/popup/device/vehicle_detail.html', locals())


class VideoPlaybackView(ParseJsonView, View):
    """回放视频View"""

    def get(self, request):
        _id = request.GET.get('id')
        url = 'http://vfx.mtime.cn/Video/2019/03/21/mp4/190321153853126488.mp4'
        return render(request, 'admin/popup/device/video_playback.html', locals())

    def post(self, request):
        """返回视频url"""
        pass


class RealTimeView(ParseJsonView, View):
    """实时监控View"""

    def get(self, request):
        return render(request, 'admin/device/other/real_time.html', locals())

    def post(self, request):
        """监控页面获取数据接口"""
        pass


class WebRtcView(ParseJsonView, View):
    """单摄像头webrtc视频流"""

    def get(self, request):
        _id = request.GET.get('id')
        if self.hash_to_pk(_id) == 1:
            device_video_url = 'http://192.168.2.84:8083/stream/6f9155485a1f85b8d2d801badf7ae09b/channel/0/webrtc?uuid=6f9155485a1f85b8d2d801badf7ae09b&channel=0&device_id=%s' % _id
        else:
            device_video_url = 'http://192.168.2.84:8083/stream/580cfe817d3cf0ea2edc98e36e356642/channel/0/webrtc?uuid=580cfe817d3cf0ea2edc98e36e356642&channel=0&device_id=%s' % _id
        return render(request, 'admin/device/other/webrtc.html', locals())
