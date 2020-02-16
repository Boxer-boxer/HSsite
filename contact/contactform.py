from django import forms
from .models import contact

class ContactForm(forms.ModelForm):
	mensagem = forms.CharField(widget=forms.Textarea())

	class Meta:
		model = contact
		fields = ['nome_completo', 'email', 'mensagem']