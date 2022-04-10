# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: admin_view.py
@time: 2022/4/7 10:55
"""

from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator

from apps.archives import models
from apps.public.views import ParseJsonView


class SearchPersonnelView(ParseJsonView, View):
    """以人搜图View"""

    def get(self, request):
        """以人搜图模板"""
        current_page = 1
        page_size = 10
        library_page = Paginator(models.ArchivesGroup.objects.order_by('-id'), page_size)
        if library_page.page_range.start <= current_page <= library_page.page_range.stop:
            library_list = library_page.page(current_page).object_list
            return render(request, 'admin/archives/other/search_person.html', locals())

    def post(self, request):
        """数据返回"""
        return


class AccessPassDetailView(ParseJsonView, View):
    """门禁人员通行详情View"""

    def get(self, request):
        """门禁通行详情模板"""
        _id = request.GET.get('id')
        detail_type = request.GET.get('detail_type')
        instance = models.AccessDiscover.objects.get(id=self.hash_to_pk(_id))
        return render(request, 'admin/popup/archives/access_pass_detail.html', locals())
