"""
ASGI config for stock_p project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from stock_a import routing
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_p.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(routing.ws_urlpatterns))
})