from django.db import models
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
    


