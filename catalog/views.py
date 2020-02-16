from django.shortcuts import render, redirect
from catalog.models import Item
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from .catalogfilters import CatalogFilters


from users.models import Cart

class CatalogListView(ListView):
	model = Item
	template_name = 'catalog/catalog.html'
	context_object_name = 'Item'
	paginate_by = 1
	ordering = ['-date_added']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = CatalogFilters(self.request.GET, queryset=self.get_queryset())
		return context

class ItemDetailView(DetailView):
	model = Item
	template_name = 'catalog/detail.html'
	context_object_name = 'Item'

	def get_context_data(self, *args, **kwargs):
		context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj

		return context


def enter(request):
	return render(request, 'catalog/enter.html')

def home(request):
	random_item1 = Item.objects.all().order_by('?')[:4]
	random_item2 = Item.objects.all().order_by('?')[:4]
	return render(request, 'catalog/home.html', {'Item1': random_item1, 'Item2':random_item2 })

class home_catalog(ListView):
	model = Item
	template_name = 'catalog/snippets/catalog_preview.html'
	context_object_name = 'Item'


def about(request):
	return render(request, 'catalog/about.html')
