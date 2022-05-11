# -*- coding: utf-8 -*-

"""
@author: Mr_zhang
@software: PyCharm
@file: urls.py
@time: 2022/3/7 15:36
"""

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from apps.archives import views
from apps.archives import admin_view

router = DefaultRouter()
router.register(r"group", views.ArchivesGroupViewSet, basename="group")
router.register(r"personnel", views.PersonnelViewSet, basename="personnel")

urlpatterns = [
    path(
        "search_person/",
        csrf_exempt(admin_view.SearchPersonnelView.as_view()),
        name="search_person",
    ),
    path(
        "access_pass_detail/",
        csrf_exempt(admin_view.AccessPassDetailView.as_view()),
        name="access_pass_detail",
    ),
]

urlpatterns += router.urls
