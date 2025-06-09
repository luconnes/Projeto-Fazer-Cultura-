from django.shortcuts import render, redirect
from .models import Usuarios

def home(request):
    return render(request, "usuarios/home.html")

def usuarios(request):
    if request.method == 'POST':
        novo_usuario = Usuarios()
        novo_usuario.email = request.POST.get('email')
        novo_usuario.senha = request.POST.get('senha')
        novo_usuario.save()
        return redirect('listagem_usuarios')  # redireciona para evitar duplicação

    usuarios = {
        'usuarios': Usuarios.objects.all()
    }
    return render(request, 'usuarios/usuarios.html', usuarios)

# def deletar_usuarios(request):
#     Usuarios.objects.all().delete()
#     return redirect('usuarios/usuarios.html')

##def cadastro(request):


