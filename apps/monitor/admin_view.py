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

from apps.monitor import models
from apps.public.views import ParseJsonView


# Create your views here.


class PhotoClusterView(ParseJsonView, View):
    """轨迹档案View"""

    def get(self, request):
        """轨迹档案页面返回"""
        _id = request.GET.get('id')
        photo = models.ArchivesPersonnel.objects.get(id=self.hash_to_pk(_id)).get_head_url()
        return render(request, 'admin/popup/monitor/photo_search.html', locals())

    def post(self, request):
        """轨迹档案数据返回"""
        request_data = self.parse_body(request)
        current_page = request_data.get('current_page', 1)
        page_size = request_data.get('page_size', 10)
        paginate = request_data.get('paginate')
        _id = request_data.get('id')
        _photo_list = models.PhotoCluster.objects.filter(archives_personnel_id=self.hash_to_pk(_id)).order_by('-id').values()
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class PhotoDetailView(ParseJsonView, View):
    """档案详情View"""
    def get(self, request):
        """轨迹档案详情"""
        _id = request.GET.get('id')
        instance = models.PhotoCluster.objects.get(id=self.hash_to_pk(_id))
        return render(request, 'admin/popup/monitor/photo_detail.html', locals())


class VehicleSearchView(ParseJsonView, View):
    """重点车辆抓拍View"""

    def get(self, request):
        """模板返回"""
        _id = request.GET.get('id')
        return render(request, 'admin/popup/monitor/vehicle_search.html', locals())

    def post(self, request):
        """重点车辆数据返回"""
        request_data = self.parse_body(request)
        current_page = request_data.get('current_page', 1)
        page_size = request_data.get('page_size', 10)
        paginate = request_data.get('paginate')
        _id = request_data.get('id')
        # _photo_list = models.VehicleMonitorDiscover.objects.filter(target_id=_id).order_by('-id').values('id', 'target__plate', 'record__device__name', 'record__address', 'record__take_photo_time', 'record__plate_path')
        _photo_list = models.VehicleMonitorDiscover.objects.order_by('-id').values('id', 'target__plate', 'record__device__name', 'record__address', 'record__take_photo_time', 'record__plate_path')
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class VehicleDetailView(ParseJsonView, View):
    """车辆预警系详情View"""

    def get(self, request):
        _id = request.GET.get('id')
        instance = models.VehicleMonitorDiscover.objects.get(id=self.hash_to_pk(_id))
        return render(request, 'admin/popup/monitor/vehicle_detail.html', locals())