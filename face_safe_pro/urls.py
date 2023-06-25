"""face_safe_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.urls import include
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.staticfiles.views import serve
from rest_framework.documentation import include_docs_urls

from public import views as public_view

urls_v1 = [
    path("account/", include(("account.urls", "account"))),
    path("archives/", include(("archives.urls", "archives"))),
    path("device/", include(("device.urls", "device"))),
    path("monitor/", include(("monitor.urls", "monitor"))),
    path("public/", include(("public.urls", "public"))),
]

if settings.BIG_SCREEN:
    urls_v1.append(
        path("telecom/", include(("telecom.urls", "telecom"))),
    )

urlpatterns = [
    re_path(r"^static/(?P<path>.*)$", serve, name="static"),  # 静态文件
    path("web_upload/", public_view.web_upload_image, name="web_upload"),
    path("f_upload/<file_types>/", public_view.upload_image),
    path("v1/", include(urls_v1)),  # RestApi
    path("favicon.ico", RedirectView.as_view(url=r"static/favicon.ico")),  # favicon
    path("admin/", admin.site.urls, name="admin"),  # admin管理后台
    path("sp/", include("simplepro.urls")),  # simplepro
    path(
        "api-docs/",
        include_docs_urls(
            title="智能视图平台API文档", authentication_classes=[], permission_classes=[]
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "智能视图平台"
admin.site.site_title = "智能视图平台"
# admin.site.empty_value_display = None
