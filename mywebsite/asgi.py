import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # Certifique-se que o app "chat" está listado no INSTALLED_APPS

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

# Define a aplicação ASGI para lidar com requisições HTTP e WebSocket
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Lida com requisições HTTP padrão
    "websocket": AuthMiddlewareStack(  # Lida com WebSocket, com autenticação
        URLRouter(
            chat.routing.websocket_urlpatterns  # Roteia as conexões WebSocket
        )
    ),
})