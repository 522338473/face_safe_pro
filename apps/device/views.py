from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator

from apps.device import models
from apps.public.views import ParseJsonView


# Create your views here.


class PhotoSearchView(ParseJsonView, View):
    """以图搜图模块接口"""

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
        _photo_list = models.DevicePhoto.objects.filter(id=_id).order_by('-id').values()
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class PhotoDetailView(ParseJsonView, View):

    def get(self, request):
        """以图搜图页面详情"""
        _id = request.GET.get('id')
        instance = models.DevicePhoto.objects.get(id=_id)
        return render(request, 'admin/popup/device/photo_detail.html', locals())


class SearchImageView(ParseJsonView, View):
    """以图搜图接口"""

    def get(self, request):
        """以图搜图模板返回"""
        current_page = 1
        page_size = 10
        photo_page = Paginator(models.DevicePhoto.objects.order_by('-id'), page_size)
        if photo_page.page_range.start <= current_page < photo_page.page_range.stop:
            photo_list = photo_page.page(current_page).object_list
            return render(request, 'admin/device/other/search_image.html', locals())

    def post(self, request):
        """以图搜图数据返回"""
        pass


class VehicleSearchView(ParseJsonView, View):
    """机动车查询"""

    def get(self, request):
        _id = request.GET.get('id')
        return render(request, 'admin/popup/device/vehicle_search.html', locals())

    def post(self, request):
        request_data = self.parse_body(request)
        current_page = request_data.get('current_page', 1)
        page_size = request_data.get('page_size', 10)
        paginate = request_data.get('paginate')
        _id = request_data.get('id')
        _plate = models.Vehicle.objects.get(id=_id).plate
        _photo_list = models.Vehicle.objects.filter(plate=_plate).order_by('-id').values('device__name', 'address', 'take_photo_time', 'plate_path')
        photo_page = Paginator(_photo_list, page_size)
        if photo_page.page_range.start <= current_page <= photo_page.page_range.stop:
            return self.paginate_response(photo_page, current_page, paginate)


class VehicleDetailView(ParseJsonView, View):
    """机动车详情"""

    def get(self, request):
        _id = request.GET.get('id')
        instance = models.Vehicle.objects.get(id=_id)
        return render(request, 'admin/popup/device/vehicle_detail.html', locals())


class VideoPlaybackView(ParseJsonView, View):
    """回放视频接口"""

    def get(self, request):
        return render(request, 'admin/popup/device/video_playback.html', locals())


class RealTimeView(ParseJsonView, View):
    """实时监控页面"""

    def get(self, request):
        current_page = 1  # self.get_current_page(request, 1)
        page_size = 10  # self.get_page_size(request, 10)
        device_page = Paginator(models.DeviceInfo.objects.order_by('id'), page_size)
        if device_page.page_range.start <= current_page < device_page.page_range.stop:
            device_list = device_page.page(current_page).object_list
            return render(request, 'admin/device/other/real_time.html', locals())

    def post(self, request):
        """监控页面获取数据接口"""
        pass
