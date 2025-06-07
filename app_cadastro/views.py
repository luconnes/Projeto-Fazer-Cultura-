from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios


# Página inicial
def home(request):
    return render(request, "usuarios/login.html")


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios
from .forms import UsuarioForm  # importa o form

# Página inicial
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

            form.instance.senha = make_password(senha)
            form.save()
            return redirect('login')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


# Login do usuário
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Usuarios

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

    # Aqui está o ajuste importante:
    return render(request, 'usuarios/login.html', {'exibir_navbar': False})


# Logout
def logout(request):
    request.session.flush()
    return redirect('login')


# Painel do usuário (após login)
def painel(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    return render(request, 'usuarios/painel.html', {
        'email': request.session.get('usuario_email')
    })


# Listagem de todos os usuários (admin, por exemplo)
def listagem_usuarios(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})


# Sala de chat
def lobby(request):
    return render(request, 'chat/lobby.html')
