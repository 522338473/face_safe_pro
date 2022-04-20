import json
import time
import base64
import requests

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ParseError

from apps.utils.hasher import Hasher
from apps.utils.constant import FILE_PATH_PREFIX


class HashRetrieveViewSetMixin(GenericViewSet):
    """使用Hash检索对象的ViewSet基类"""

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = self.get_obj_from_hash(self.kwargs['pk'], queryset)
        self.check_object_permissions(self.request, obj)

        return obj

    def get_obj_from_hash(self, hash_id, queryset):
        """根据hash_id获取obj对象"""
        pk = self.hash_to_pk(hash_id)
        obj = get_object_or_404(queryset, pk=pk)
        return obj

    @staticmethod
    def hash_to_pk(hash_id):
        """Hash 转 id"""
        try:
            pk = Hasher.to_object_pk(hash_id)
        except ValueError:
            raise ParseError('parse error')
        return pk

    @staticmethod
    def pk_to_hash(pk):
        """id 转 Hash"""
        try:
            hs = Hasher.make_hash(pk)
        except ValueError:
            raise ParseError('parse error')
        return hs


class ParseJsonView:

    def get_current_page(self, request, default=1):
        """获取当前页码"""
        return self.parse_body(request).get('current_page', default)

    def get_page_size(self, request, default=None):
        return self.parse_body(request).get('page_size', default)

    @staticmethod
    def parse_body(request):
        return json.loads(request.body)

    @staticmethod
    def paginate_response(paginate_queryset, current_page=1, paginate='on'):
        """
        返回数据封装
        :param paginate_queryset: queryset分页对象
        :param current_page: 当前页
        :param paginate: 是否分页
        :return:
        """
        if paginate == 'off':
            return JsonResponse(list(paginate_queryset.object_list), safe=False)
        else:
            data = {
                'count': paginate_queryset.count,
                'results': list(paginate_queryset.page(current_page).object_list)
            }
            return JsonResponse(data, safe=False)

    @staticmethod
    def hash_to_pk(hash_id):
        """Hash 转 id"""
        try:
            pk = Hasher.to_object_pk(hash_id)
        except ValueError:
            pk = hash_id
        except Exception:
            raise ParseError('parse error')
        return pk


def page_not_found(request, *args, **kwargs):
    return render(request, '404/404.html')


@csrf_exempt
def upload_image(request, file_types=None):
    """自定义文件上传"""
    res_upload = {
        'success': 1,
        'message': '上传成功哈哈哈',
        'url': None
    }
    if not file_types:  # 默认抓拍抓拍路径
        path = ''.join([FILE_PATH_PREFIX, '/snap/', time.strftime('%Y/%m/%d', time.localtime())])
    elif file_types == 'archives':  # 人员档案路径
        path = ''.join([FILE_PATH_PREFIX, '/archives/'])
    elif file_types == 'monitor':  # 重点人员路径
        path = ''.join([FILE_PATH_PREFIX, '/monitor/'])
    elif file_types == 'personnel':  # 关注人员路径
        path = ''.join([FILE_PATH_PREFIX, '/personnel/'])
    else:
        path = ''.join([FILE_PATH_PREFIX, '/other/'])
    file = request.FILES.get('file')
    if isinstance(file, InMemoryUploadedFile):
        file = base64.b64encode(file.read()).decode()

    photo = base64.b64decode(file)
    files = {'file': photo}
    options = {
        'output': 'json',
        'path': path,
        'scene': ''
    }
    res = requests.post('http://192.168.2.95:8089/upload', data=options, files=files).json()
    res_upload['url'] = res['path']
    return JsonResponse(res_upload)


@csrf_exempt
def web_upload_image(request, *args, **kwargs):
    """浏览器上传"""
    res_upload = {
        'success': 1,
        'message': '上传成功哈哈哈',
        'url': None
    }
    file = request.FILES.get('file')
    path = ''.join([FILE_PATH_PREFIX, '/other/'])
    if isinstance(file, InMemoryUploadedFile):
        file = base64.b64encode(file.read()).decode()

    photo = base64.b64decode(file)
    files = {'file': photo}
    options = {
        'output': 'json',
        'path': path,
        'scene': ''
    }
    res = requests.post('http://192.168.2.95:8089/upload', data=options, files=files).json()
    res_upload['url'] = res['url']
    return JsonResponse(res_upload)
