from django.db import models
import datetime

class Catalog(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Item(models.Model):
	TYPE_MATERIAL = (
		('OURO', 'Ouro'),
		('PRTA', 'Prata'),
		('AÇOS', 'Aços')
		)

	TYPE_ITEM = (
		('ANÉIS','Anéis'),
		('COLARES','Colares'),
		('BRINCOS','Brincos'),
		('RELÓGIOS','Relógios'),
		('PULSEIRAS','Pulseiras'),
		('OUTROS','Outros'),
		)

	TYPE_FORNECEDOR = (
		('Fornecedor1','Fornecedor1'),
		('Fornecedor2','Fornecedor2'),
		('Fornecedor3','Fornecedor3'),
		('Fornecedor4','Fornecedor4'),
		('Fornecedor5','Fornecedor5'),
		('Fornecedor6','Fornecedor6'),
		('Fornecedor7','Fornecedor7'),
		)

	TYPE_PRICE = (
		('0.50 - 5.00', '0.50 - 5.00'),
		('6.00 - 20.00', '6.00 - 20.00'),
		('21.00 - 50.00', '21.00 - 50.00'),
		('51.00 - 100.00', '51.00 - 100.00'),
		('101.00 - 200.00', '101.00 - 200.00'),
		('201.00 - 300.00', '201.00 - 300.00'),
		('301.00 - 400.00', '301.00 - 400.00'),
		('401.00 - 500.00', '401.00 - 500.00'),
		('501.00 - 600.00', '501.00 - 600.00'),
		('601.00 - 700.00', '601.00 - 700.00'),
		('701.00 - 800.00', '701.00 - 800.00'),
		('801.00 - 900.00', '801.00 - 900.00'),
		('901.00 - 1000.00', '901.00 - 1000.00'),
		('1001.00 - 2000.00', '1001.00 - 2000.00'),
		('2001.00 - 5000.00', '2001.00 - 5000.00'),
		)

	type_material = models.CharField(max_length=5, choices=TYPE_MATERIAL, default='')
	type_item = models.CharField(max_length=10, choices=TYPE_ITEM, default='')
	type_fornecedor = models.CharField(max_length=30, choices=TYPE_FORNECEDOR, default='')
	type_price = models.CharField(max_length=40, choices=TYPE_PRICE, default='')
	reference = models.CharField(max_length=50)
	price = models.FloatField()
	image_1 = models.ImageField(default='transferir', upload_to='static/catalog')
	image_2 = models.ImageField(default='transferir', upload_to='static/catalog')
	image_3 = models.ImageField(default='transferir', upload_to='static/catalog')
	image_4 = models.ImageField(default='transferir', upload_to='static/catalog')
	catalog = models.ForeignKey(Catalog, on_delete= models.DO_NOTHING, default='')
	is_hidden = models.BooleanField(default=False)
	date_added = models.DateTimeField(auto_now_add=True)
	tamanho = models.CharField(max_length=3, default='0')

#	class meta:
#		ordering = ['-date_added']

	def __str__(self):
		return self.reference


