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

from device import views
from device import admin_view

router = DefaultRouter()
router.register(r"info", views.DeviceInfoViewSet, basename="info")
router.register(r"photo", views.DevicePhotoViewSet, basename="photo")
router.register(r"vehicle", views.VehicleViewSet, basename="vehicle")
router.register(r"motor", views.MotorViewSet, basename="motor")
router.register(r"offline", views.DeviceOffLineViewSet, basename="offline")

urlpatterns = [
    path(
        "vehicle_search/",
        csrf_exempt(admin_view.VehicleSearchView.as_view()),
        name="vehicle_search",
    ),
    path(
        "vehicle_detail/",
        csrf_exempt(admin_view.VehicleDetailView.as_view()),
        name="vehicle_detail",
    ),
    path(
        "video_playback/",
        csrf_exempt(admin_view.VideoPlaybackView.as_view()),
        name="video_playback",
    ),
    path(
        "photo_search/",
        csrf_exempt(admin_view.PhotoSearchView.as_view()),
        name="photo_search",
    ),
    path(
        "photo_detail/",
        csrf_exempt(admin_view.PhotoDetailView.as_view()),
        name="photo_detail",
    ),
    path(
        "search_image/",
        csrf_exempt(admin_view.SearchImageView.as_view()),
        name="search_image",
    ),
    path(
        "real_time/", csrf_exempt(admin_view.RealTimeView.as_view()), name="real_time"
    ),
    path("webrtc/", csrf_exempt(admin_view.WebRtcView.as_view()), name="webrtc"),
]

urlpatterns += router.urls
