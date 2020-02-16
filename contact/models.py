from django.db import models

# Create your models here.

class contact(models.Model):
	nome_completo = models.CharField(max_length=50, default='')
	email = models.EmailField()
	mensagem = models.CharField(max_length= 550)

	def __str__(self):
		return f'{self.nome_completo}'