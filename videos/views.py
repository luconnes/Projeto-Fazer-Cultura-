from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .models import Video, Avaliacao # Importe Video e Avaliacao
from app_cadastro.models import Usuarios # Importe Usuarios
# Create your views here.

@login_required(login_url='login') # Garante que apenas usuários logados possam acessar
@require_POST # Aceita apenas requisições POST
def avaliar_video(request):
    # Verifica se o usuário está logado usando a sessão personalizada
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return JsonResponse({'status': 'error', 'message': 'Usuário não autenticado.'}, status=401)

    try:
        data = json.loads(request.body)
        video_id = data.get('video_id')
        nota = data.get('nota')
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Dados JSON inválidos.'}, status=400)

    if not video_id or not nota:
        return JsonResponse({'status': 'error', 'message': 'ID do vídeo e nota são obrigatórios.'}, status=400)

    try:
        video = get_object_or_404(Video, id=video_id)
        usuario = get_object_or_404(Usuarios, id_usuario=usuario_id)

        # Tenta encontrar uma avaliação existente do usuário para este vídeo
        avaliacao_existente = Avaliacao.objects.filter(video=video, usuario=usuario).first()

        if avaliacao_existente:
            # Se já existe, atualiza a nota
            avaliacao_existente.nota = nota
            avaliacao_existente.save()
            message = 'Avaliação atualizada com sucesso!'
        else:
            # Se não existe, cria uma nova avaliação
            Avaliacao.objects.create(video=video, usuario=usuario, nota=nota)
            message = 'Avaliação registrada com sucesso!'

        # Recalcula a média de todas as avaliações para este vídeo
        # Mesmo que video.avaliacao seja IntegerField, calculamos a média float para exibir no frontend
        avaliacoes_do_video = Avaliacao.objects.filter(video=video)
        if avaliacoes_do_video.exists():
            soma_das_notas = sum([a.nota for a in avaliacoes_do_video])
            quantidade_avaliacoes = avaliacoes_do_video.count()
            media_calculada = soma_das_notas / quantidade_avaliacoes

            # Atualiza o campo 'avaliacao' no modelo Video (será truncado para int)
            video.avaliacao = int(round(media_calculada)) # Arredonda para o inteiro mais próximo
        else:
            video.avaliacao = 0 # Nenhuma avaliação
        video.save()

        # Retorna a média calculada (float) para o frontend exibir formatada
        return JsonResponse({'status': 'success', 'message': message, 'nova_media': media_calculada})

    except Video.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Vídeo não encontrado.'}, status=404)
    except Usuarios.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado.'}, status=404)
    except Exception as e:
        print(f"Erro ao avaliar vídeo: {e}") # Para depuração
        return JsonResponse({'status': 'error', 'message': 'Erro interno do servidor.'}, status=500)