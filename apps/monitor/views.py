from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator

from apps.monitor import models
from apps.public.views import ParseJsonView


# Create your views here.


class PhotoClusterView(ParseJsonView, View):
    """轨迹档案接口"""

    def get(self, request):
        """轨迹档案页面返回"""
        _id = request.GET.get('id')
        personnel_path = models.ArchivesPersonnel.objects.get(id=_id).photo
        return render(request, 'admin/popup/monitor/photo_search.html', locals())

    def post(self, request):
        """轨迹档案数据返回"""
        request_data = self.parse_body(request)
        current_page = request_data.get('current_page', 1)
        page_size = request_data.get('page_size', 10)
        paginate = request_data.get('paginate')
        _id = request_data.get('id')
        _photo_list = models.PhotoCluster.objects.filter(archives_personnel_id=_id).order_by('-id').values()
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class PhotoDetailView(ParseJsonView, View):

    def get(self, request):
        """轨迹档案详情"""
        _id = request.GET.get('id')
        instance = models.PhotoCluster.objects.get(id=_id)
        return render(request, 'admin/popup/monitor/photo_detail.html', locals())


class VehicleSearchView(ParseJsonView, View):
    """重点车辆抓拍记录"""

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
        _photo_list = models.VehicleMonitorDiscover.objects.filter(target_id=_id).order_by('-id').values('id', 'target__plate', 'record__device__name', 'record__address', 'record__take_photo_time', 'record__plate_path')
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class VehicleDetailView(ParseJsonView, View):
    """车辆预警系详情"""

    def get(self, request):
        _id = request.GET.get('id')
        instance = models.VehicleMonitorDiscover.objects.get(id=_id)
        return render(request, 'admin/popup/monitor/vehicle_detail.html', locals())
