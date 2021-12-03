import os
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from batches.channels.consumers import BatchConsumer

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "True"

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("batch/room/", BatchConsumer.as_asgi(), ),
            ]
        )
    )
})
