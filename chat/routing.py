from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws://${window.location.host}/ws/socket-server/', consumers.ChatConsumer.as_asgi()),
]
