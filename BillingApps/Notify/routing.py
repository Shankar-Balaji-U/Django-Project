from django.urls import re_path
from Notify.consumers import NotificationConsumer



wsspatterns = [
    re_path('websocket/notify/', NotificationConsumer.as_asgi()),
]