"""
ASGI config for face_safe_pro project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.telecom.routing import websocket_urlpatterns as telecom_websocket_urlpatterns
from apps.public.routing import websocket_urlpatterns as public_websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "face_safe_pro.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(telecom_websocket_urlpatterns + public_websocket_urlpatterns)
        ),
    }
)
