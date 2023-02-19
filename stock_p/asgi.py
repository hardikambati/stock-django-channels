"""
ASGI config for stock_p project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_p.settings')

django_asgi_app = get_asgi_application()

from stock_a import routing
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter(routing.ws_urlpatterns))
})