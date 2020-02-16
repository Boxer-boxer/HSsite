from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User

from catalog.models import Item
from .models import Cart
from .forms import UserRegisterForm

from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def Register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			messages.success(request, f'A conta com o username: {username}, foi criada!')
			return redirect('login')

	else:
		form = UserRegisterForm()

	return render(request, 'users/register.html', { 'form': form })


def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	key = settings.STRIPE_PUBLISHABLE_KEY
	return render(request, 'users/cart_home.html', {'cart': cart_obj, 'key': key})

def cart_update(request):

	print(request.POST)

	product_id = request.POST.get('product_id')

	if product_id is not None:
		try:
			obj = Item.objects.get(id=product_id)
			print(product_id)
		except Item.DoesNotExist:
			print('Item does not exist!')
			return redirect('home')

		cart_obj, new_obj = Cart.objects.new_or_get(request)

		if obj in cart_obj.products.all():
			cart_obj.products.remove(obj)
		else:
			cart_obj.products.add(obj)

	return redirect('cart_home')

