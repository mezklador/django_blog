from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

class Category(models.Model):
    label = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=550)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse("category_detail",
                       kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['-created_at', '-updated_at']


def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.label)
    if new_slug is not None:
        slug = new_slug
    qs = Category.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        the_id = int(qs.first().id) + 1
        the_new_slug = "{}-{}".format(slug, str(the_id))
        return create_slug(instance, new_slug=the_new_slug)

    return slug

pre_save.connect(pre_save_category_receiver, Category)
