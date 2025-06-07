from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('usuarios/', views.listagem_usuarios, name='listagem_usuarios'),
    path('chat/', views.lobby, name='chat'),
    ##path('login/', views.login, name='login'),
    path('cadastro/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('logout/', views.logout, name='logout'),
    path('painel/', views.painel, name='painel'),
]
