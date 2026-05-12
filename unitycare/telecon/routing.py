from django.urls import re_path
from .consumers import TeleconConsumer

websocket_urlpatterns = [
    re_path(r"^ws/telecon/(?P<room_name>[^/]+)/?$", TeleconConsumer.as_asgi()),
]