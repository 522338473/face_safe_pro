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

from apps.device import models
from apps.device import serializers
from apps.public.views import ParseJsonView


# Create your views here.


class PhotoSearchView(ParseJsonView, View):
    """以图搜图模块View"""

    def get(self, request):
        """以图搜图页面返回"""
        _id = request.GET.get('id')
        return render(request, 'admin/popup/device/photo_search.html', locals())

    def post(self, request):
        """以图搜图数据获取"""
        request_data = self.parse_body(request)
        current_page = request_data.get('current_page', 1)
        page_size = request_data.get('page_size', 10)
        paginate = request_data.get('paginate')
        _id = request_data.get('id')
        # _photo_list = models.DevicePhoto.objects.filter(id=_id).order_by('-id').values()
        _photo_list = models.DevicePhoto.objects.order_by('-id').values()
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class PhotoDetailView(ParseJsonView, View):
    """照片详情View"""

    def get(self, request):
        """以图搜图页面详情"""
        _id = request.GET.get('id')
        instance = models.DevicePhoto.objects.get(id=self.hash_to_pk(_id))
        return render(request, 'admin/popup/device/photo_detail.html', locals())


class SearchImageView(ParseJsonView, View):
    """以图搜图View"""

    def get(self, request):
        """以图搜图模板返回"""
        return render(request, 'admin/device/other/search_image.html', locals())


def post(self, request):
    """以图搜图数据返回"""
    pass


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
        _plate = models.Vehicle.objects.get(id=self.hash_to_pk(_id)).plate
        # _photo_list = models.Vehicle.objects.filter(plate=_plate).order_by('-id').values('id', 'device__name', 'address', 'take_photo_time', 'plate_path')
        _photo_list = models.Vehicle.objects.order_by('-id').values('id', 'device__name', 'address', 'take_photo_time', 'plate_path')
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class VehicleDetailView(ParseJsonView, View):
    """机动车详情View"""

    def get(self, request):
        _id = request.GET.get('id')
        instance = models.Vehicle.objects.get(id=self.hash_to_pk(_id))
        return render(request, 'admin/popup/device/vehicle_detail.html', locals())


class VideoPlaybackView(ParseJsonView, View):
    """回放视频View"""

    def get(self, request):
        _id = request.GET.get('id')
        print(_id)
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
