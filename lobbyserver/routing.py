from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/livegame/(?P<game_id>\d+)$', consumers.GameConsumer.as_asgi()),
    re_path(r'ws/$',consumers.MenuConsumer.as_asgi())
]
#(?P<game_id>\d+)