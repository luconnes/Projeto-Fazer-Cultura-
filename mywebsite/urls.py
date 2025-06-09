# mywebsite/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_cadastro.urls')),  # home e cadastro de usuários
    path('chat/', include('chat.urls')),     # página do chat
    path('videos/', include('videos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
