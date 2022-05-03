"""
ASGI config for lobbychessserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django #
from django.conf import settings #
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
import lobbyserver.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lobbychessserver.settings')
if not settings.configured: #
    django.setup()          #
#application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            lobbyserver.routing.websocket_urlpatterns
        )
    ),
})