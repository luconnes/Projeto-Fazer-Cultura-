from django.db import models

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    email = models.TextField(max_length=100)
    senha = models.TextField(max_length=30)

    