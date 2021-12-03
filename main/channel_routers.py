import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from batches.consumers import BatchConsumer

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "True"

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        URLRouter(
            [

            ]
        )
    )
})
