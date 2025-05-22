# app_cadastro/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('usuarios/', views.usuarios, name='listagem_usuarios'),
    path('chat/',views.lobby, name='chat')
    # path('usuarios/limpar/', views.deletar_usuarios, name='deletar_usuarios'),
]
