from django.shortcuts import render, redirect
from django.views.generic import TemplateView,  CreateView, DetailView, UpdateView
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.template import loader
from django.contrib import messages

from datetime import datetime
from string import ascii_uppercase
from random import randint

from users.models import Cart
from catalog.models import Item
from .models import Order, Profile


import stripe

date = str(datetime.now())[:10].split('-')
hour = str(datetime.now())[11:16].split(':')
order_id = ''.join(date)+''.join(hour)+ascii_uppercase[randint(0,20)]+ascii_uppercase[randint(0,20)]+str(randint(0,100))+str(randint(0,100))+'Order'

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderCreateView(CreateView):

	model = Order
	fields = ['nome_completo', 'email', 'rua', 'andar', 'numero', 'localidade', 'distrito', 'codigo_postal_1', 'codigo_postal_2']

	def form_valid(self, form):

		cart_obj, new_obj = Cart.objects.new_or_get(self.request)

		self.object = form.save(commit=False)
		if self.request.user.is_authenticated:
			self.object.user = self.request.user
		else:
			self.object.user= User.objects.get(username='DummyUser')
		self.object.cart = cart_obj
		self.object.order_id = order_id
		self.object.total = cart_obj.subtotal
		self.object.save()


		return HttpResponseRedirect(self.get_success_url())

class OrdereditView(UpdateView):
	model = Order
	fields = ['nome_completo', 'email', 'rua', 'numero', 'andar', 'localidade', 'distrito', 'codigo_postal_1', 'codigo_postal_2']
	template_name_suffix = '_update_form'

def OrderDetailView(request, slug):

	order = get_object_or_404(Order, slug=slug)
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	template = 'payments/orderdetail.html'

	context = {'order': order}

	return render(request, template, context)

def OrderFinal(request, slug):
	order = get_object_or_404(Order, slug=slug)
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	template = 'payments/orderfinish.html'

	if 'Online' in request.POST:
	    for product in cart_obj.products.all():
	        if product.is_hidden == False:
        		order.ordered_through = 'online'
        		order.is_ordered = True
        		product_list = list(cart_obj.products.all()) #This does return the reference.
        		order.items = product_list
        		order_total = order.total*100

	        	order.save()
	        	context = {'order': order, 'key': settings.STRIPE_PUBLISHABLE_KEY, "total": order_total}

	        	return render(request, template, context)
	        else:
	            messages.error(request, 'Erro: Por alguma razão, não foi possível realizar a sua encomenda. Um ou mais dos produtos que tentou encomendar podem estar indisponíveis ou foram encomendados por outro cliente. Removemos este produto do seu carrinho. Caso o seu carrinho ainda tenha produtos, por favor, volte a tentar encomendar. Em caso de dúvidas, por favor, entre em contacto connosco.')
	            context = {'order':order}
	            cart_obj.products.remove(product)
	            return redirect('cart_home')


def charge(request, slug):
	order = get_object_or_404(Order, slug=slug)
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	template = 'payments/charge.html'
	if request.method == 'POST':
		charge = stripe.Charge.create(
        	amount= order.total*100,
        	currency='eur',
			description=f'{order.id}',
			source=request.POST['stripeToken']
		)
		messages.success(request, 'A sua encomenda foi registada! Os produtos serão enviados assim que confirmarmos o pagamento. Em caso de dúvidas, não hesite em contactar-nos')
	for obj in cart_obj.products.all():
		cart_obj.products.remove(obj)
		if obj in Item.objects.all():
		    obj.is_hidden=True
		    obj.save()

	return render(request, template, {"order":order})


def OrderConfirmed(request, slug):
    order = get_object_or_404(Order, slug=slug)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    template = 'payments/orderfinal.html'

    if 'CTT' in request.POST:
        for product in cart_obj.products.all():
            if product.is_hidden == False:
                order.ordered_through = 'ctt'
                order.is_ordered = True
                product_list = list(cart_obj.products.all())
                order.items = product_list

                order.save()

                mhemail = settings.EMAIL_HOST_USER
                subject = f'Confirmação de encomenda-{order.slug}'
                message = f' Olá, {order.nome_completo} \n Obrigado por ter feito uma encomenda! \n O producto que encomendou tem a seguinte referência: \n {str(order.items)} \n Será enviado para a morada: {order.rua}, nº {order.numero}, {order.andar}, {order.localidade}, {order.distrito} \n \n O total a pagar é {str(order.total)}.00€ \n O pagamento deverá ser efetuado aquando receber a encomenda, caso contrário, o produto será devolvido.'
                from_email = mhemail

                send_mail(subject, message, from_email, [order.email, mhemail])
                messages.success(request, 'A sua encomenda foi registada! Os produtos serão enviados a contra-reembolso. Em caso de dúvidas, não hesite em contactar-nos')

                for obj in cart_obj.products.all():
                    cart_obj.products.remove(obj)
                    if obj in Item.objects.all():
                        obj.is_hidden=True
                        obj.save()

                context = {'order': order}

                return render(request, template, context)


            else:
                messages.error(request, 'Erro: Por alguma razão, não foi possível realizar a sua encomenda. Um ou mais dos produtos que tentou encomendar podem estar indisponíveis ou foram encomendados por outro cliente. Removemos este produto do seu carrinho. Caso o seu carrinho ainda tenha produtos, por favor, volte a tentar encomendar. Em caso de dúvidas, por favor, entre em contacto connosco.')
                context = {'order':order}
                cart_obj.products.remove(product)

                return redirect('cart_home')



def ProfileView(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    else:
        order = Order.objects.all().filter(user=user)[0:].order_by('-timestamp')
        context = {
	        'user':user,
            'order':order,
        }
        template = 'payments/profile.html'
        return render(request, template, context)



def ProfileOrderView(request, slug):
	order = get_object_or_404(Order, slug=slug)
	template = "payments/profile_order.html"
	context = {'order':order}
	return render(request, template, context)
