# mywebsite/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_cadastro.urls')),  # home e cadastro de usuários
    path('chat/', include('chat.urls')),     # página do chat
    
]
