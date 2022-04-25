# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: admin_view.py
@time: 2022/4/7 10:55
"""

from django.views import View
from django.shortcuts import render

from apps.archives import models
from apps.public.views import ParseJsonView


class SearchPersonnelView(ParseJsonView, View):
    """以人搜图View"""

    def get(self, request):
        """以人搜图模板"""
        return render(request, 'admin/archives/other/search_person.html', locals())


class AccessPassDetailView(ParseJsonView, View):
    """门禁人员通行详情View"""

    def get(self, request):
        """门禁通行详情模板"""
        _id = request.GET.get('id')
        detail_type = request.GET.get('detail_type')
        instance = models.AccessDiscover.objects.get(id=self.hash_to_pk(_id))
        return render(request, 'admin/popup/archives/access_pass_detail.html', locals())
