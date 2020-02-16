from django.utils.text import slugify
from users.models import Cart

def unique_slug(model_instance, order_id, slug_field):
	slug = slugify(order_id)
	model_class = model_instance.__class__ #returns name of class

	while model_class._default_manager.filter(slug=slug).exists():
		object_pk = model_class._default_manager.latest('pk')
		object_pk = object_pk.pk + 1

		slug = f"{slug}-{object_pk}"

	return slug

