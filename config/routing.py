from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from .middleware import TokenAuthMiddlewareStack
from app.core.consumers import TaxiConsumer


application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            path('taxi/', TaxiConsumer),
        ])
    ),
})
