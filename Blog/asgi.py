"""
ASGI config for Blog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import os

from django.core.asgi import get_asgi_application

import posts.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')


application = get_asgi_application()


# ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': AuthMiddlewareStack(URLRouter(posts.routing.websocket_urlpatterns))

# })
