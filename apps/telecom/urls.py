"""face_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from rest_framework.routers import DefaultRouter

from apps.telecom import views

router = DefaultRouter()
router.register(r"optical", views.OpticalFiberAlarmViewSet, basename="optical")
router.register(r"algorithm", views.AlgorithmAlarmViewSet, basename="algorithm")
router.register(r"device", views.DeviceInfoViewSet, basename="device")
router.register(r"room_types", views.PersonnelTypeViewSet, basename="root_types")
router.register(r"records", views.MonitorViewSet, basename="records")
router.register(r"find-record", views.MonitorDiscoveryViewSet, basename="find-record")
router.register(
    r"roll_call_history", views.RollCallHistoryViewSet, basename="roll_call_history"
)

urlpatterns = []

urlpatterns += router.urls
