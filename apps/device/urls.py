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

from apps.device import views

router = DefaultRouter()

urlpatterns = [
    path('vehicle_search/', csrf_exempt(views.VehicleSearchView.as_view()), name='vehicle_search'),
    path('vehicle_detail/', csrf_exempt(views.VehicleDetailView.as_view()), name='vehicle_detail'),
    path('video_playback/', csrf_exempt(views.VideoPlaybackView.as_view()), name='video_playback'),
    path('photo_search/', csrf_exempt(views.PhotoSearchView.as_view()), name='photo_search'),
    path('photo_detail/', csrf_exempt(views.PhotoDetailView.as_view()), name='photo_detail'),
    path('search_image/', csrf_exempt(views.SearchImageView.as_view()), name='search_image'),
    path('real_time/', csrf_exempt(views.RealTimeView.as_view()), name='real_time')

]

urlpatterns += router.urls
