from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
import uuid
from datetime import datetime

# Create your models here.

class Cliente(models.Model):

    fb1= 'pre'
    fb2= 'pos'
    fb3= 'cus'

    FEEDBACK_CHOICES = (
    (fb1, 'pré-coaching') ,
    (fb2, 'pós-coaching'),
    (fb3, 'customizado'),
    )


    Nome = models.CharField(max_length=16)
    Email = models.EmailField()
    Observacoes = models.TextField()
    WebKey = models.UUIDField( default=uuid.uuid4, editable=False, unique= True)
    Orientador = models.ForeignKey(User)
    Status = models.BooleanField(default=False)

    FeedbackNome = models.CharField(max_length=36)
    TipoDeFeedback = models.CharField(max_length=12, choices= FEEDBACK_CHOICES, default=fb1)
    Deadline = models.DateField(null=True, blank = True)
    Arquivo = models.FileField()

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Clientes'


class Indicado(models.Model):
    Nome = models.CharField(max_length=100)
    Categoria = models.CharField(max_length=16)
    Email = models.EmailField(max_length=100)
    WebKey = models.UUIDField(default=uuid.uuid4, editable=False,  unique= True)
    QuemIndicou = models.ForeignKey(Cliente)
    Status = models.BooleanField(default=False)
    Resposta1 = models.TextField()
    Resposta2 = models.TextField()

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Indicados'

