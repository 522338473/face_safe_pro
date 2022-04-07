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

from apps.monitor import views
from apps.monitor import admin_view

router = DefaultRouter()
router.register(r'monitor_discover', views.MonitorDiscoverViewSet, basename='monitor_discover')

urlpatterns = [
    path('photo_search/', csrf_exempt(admin_view.PhotoClusterView.as_view()), name='photo_search'),
    path('photo_detail/', csrf_exempt(admin_view.PhotoDetailView.as_view()), name='photo_detail'),
    path('vehicle_search/', csrf_exempt(admin_view.VehicleSearchView.as_view()), name='vehicle_search'),
    path('vehicle_detail/', csrf_exempt(admin_view.VehicleDetailView.as_view()), name='vehicle_detail')
]

urlpatterns += router.urls
