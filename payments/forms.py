from django import forms
from .models import OrderByCTT

class OrderForm(forms.ModelForm):


	class Meta:
		model = Order
		fields = ['nome_completo', 
				'morada', 
				'codigo_postal_1', 
				'codigo_postal_2',
				]

