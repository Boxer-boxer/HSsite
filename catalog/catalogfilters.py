import django_filters 
from .models import Item

class CatalogFilters(django_filters.FilterSet):
	class Meta:
		model = Item
		fields = ('type_material', 'type_item', 'type_fornecedor', 'type_price')
