from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from users.models import Cart
from catalog.models import Item
from django.contrib.auth.models import User

from .utils import unique_slug

from datetime import datetime
from string import ascii_uppercase
from random import randint

class Order(models.Model):
	ORDERED_THROUGH = (
		('online', 'Online'),
		('ctt', 'CTT')
		)

	DISTRITO = (
		('Aveiro', 'Aveiro'),
		('Beja', 'Beja'),
		('Braga', 'Braga'),
		('Bragança', 'Bragança'),
		('Castelo Branco', 'Castelo Branco'),
		('Coimbra', 'Coimbra'),
		('Évora', 'Évora'),
		('Faro', 'Faro'),
		('Guarda', 'Guarda'),
		('Leiria', 'Leiria'),
		('Lisboa', 'Lisboa'),
		('Portalegre', 'Portalegre'),
		('Porto', 'Porto'),
		('Santarém', 'Santarém'),
		('Setúbal', 'Setúbal'),
		('Viana do Castelo', 'Viana do Castelo'),
		('Vila Real', 'Vila Real'),
		('Viseu', 'Viseu'),
		('Ilha da Madeira', 'Ilha da Madeira'),
		('Ilha de Porto Santo', 'Ilha de Porto Santo'),
		('Ilha de Santa Maria', 'Ilha de Santa Maria'),
		('Ilha de São Miguel', 'Ilha de São Miguel'),
		('Ilha Terceira', 'Ilha Terceira'),
		('Ilha da Graciosa', 'Ilha da Graciosa'),
		('Ilha de São Jorge', 'Ilha de São Jorge'),
		('Ilha do Pico', 'Ilha do Pico'),
		('Ilha do Faial', 'Ilha do Faial'),
		('Ilha das Flores', 'Ilha das Flores'),
		('Ilha do Corvo', 'Ilha do Corvo'),
		)

	order_id = models.CharField(max_length=100, null=False, default='Code_order')
	nome_completo = models.CharField(max_length=150, null=False)
	email = models.EmailField(default='')
	rua = models.CharField(max_length=300, null=False, default = '')
	numero = models.IntegerField(blank=True, null=True, default=0)
	andar = models.CharField(max_length=3 , null=True, default='0')
	localidade = models.CharField(max_length=60, null=False, default = '')
	distrito = models.CharField(choices=DISTRITO, max_length=30, null=False, default = '')
	morada = models.IntegerField(blank=True, null=True, default=0)
	codigo_postal_1 = models.CharField(max_length=4, blank=True, null=True, default='') #raise an error if codigo_postal != intenger
	codigo_postal_2 = models.CharField(max_length=3, blank=True, null=True, default='')
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
	items = models.CharField(max_length=500, null=False, default='') #, on_delete=models.SET_NULL)  #add items to the order, so we know what was being ordered
	total = models.IntegerField(blank=True, null=True)
	is_ordered = models.BooleanField(default=False)
	ordered_through = models.CharField(choices=ORDERED_THROUGH, max_length=10, null=False, default = '')
	timestamp = models.DateTimeField(auto_now_add=True)

	slug = models.SlugField(max_length=100, default='')

	def get_absolute_url(self):
		return reverse('CTT_order_detail', kwargs={'slug': self.slug})

	def __str__(self):
		return self.order_id

def slug_save(sender, instance, *args, **kwargs):
	if instance.slug == '':
		instance.slug = unique_slug(instance, instance.order_id, instance.slug)

pre_save.connect(slug_save, sender=Order)

class Profile(models.Model):
	user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
	orders = models.ForeignKey(Order, on_delete=models.DO_NOTHING)

	def __str__(self):
		return f'Perfil de {self.user.username}'

