from django.db import models
from django.db.models import Avg
from app_cadastro.models import Usuarios  # importe seu modelo personalizado

class Video(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)  # ⬅️ campo adicionado aqui
    arquivo = models.FileField(upload_to='videos/')
    data_envio = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    avaliacao = models.IntegerField(default=0)  # ⬅️ campo adicionado aqui

    def __str__(self):
        return self.titulo

    def get_media_avaliacoes(self):
        media = self.avaliacoes.aggregate(Avg('nota'))['nota__avg']
        return round(media, 1) if media is not None else 0.0

    def get_total_avaliacoes(self):
        return self.avaliacoes.count()
    
class Avaliacao(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE) # Use Usuarios, não settings.AUTH_USER_MODEL
    nota = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    class Meta:
        unique_together = ('video', 'usuario') # Garante que um usuário só avalie um vídeo uma vez

    def __str__(self):
        return f'{self.usuario.email} - {self.video.titulo} ({self.nota} estrelas)'

