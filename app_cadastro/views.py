from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios
from .forms import UsuarioForm
from videos.models import Video
from videos.forms import VideoForm
from django.db import IntegrityError



# Página inicial (login)
def home(request):
    return render(request, "usuarios/login.html")


# Cadastro de usuário
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            if Usuarios.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já está cadastrado.')
                return redirect('cadastrar_usuario')

            try:
                form.instance.senha = make_password(senha)
                form.save()
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'Erro: E-mail já cadastrado.')
                return redirect('cadastrar_usuario')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


# Login do usuário
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuarios.objects.filter(email=email).first()
        if usuario and check_password(senha, usuario.senha):
            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_email'] = usuario.email
            return redirect('painel')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')

    return render(request, 'usuarios/login.html', {'exibir_navbar': False})


# Logout
def logout(request):
    request.session.flush()
    return redirect('login')


# Painel do usuário
def painel(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    return render(request, 'usuarios/painel.html', {
        'email': request.session.get('usuario_email')
    })


# Listagem de usuários (admin)
def listagem_usuarios(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})


# Sala de chat
def lobby(request):
    return render(request, 'chat/lobby.html')


# Página de envio de vídeo
def enviar_video(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            # Aqui associamos ao usuário da sessão manualmente
            usuario_id = request.session.get('usuario_id')
            usuario = Usuarios.objects.get(id_usuario=usuario_id)
            video.usuario = usuario
            video.save()
            return redirect('lista_videos')
    else:
        form = VideoForm()

    return render(request, 'usuarios/enviar_video.html', {'form': form})


# Página de listagem de vídeos
def lista_videos(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    videos = Video.objects.all().order_by('-data_envio')
    return render(request, 'usuarios/lista_videos.html', {'videos': videos})
