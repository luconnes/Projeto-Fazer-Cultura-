# mywebsite/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('app_cadastro.urls')),  # home e cadastro de usuários
    path('chat/', include('chat.urls')),     # página do chat
]
