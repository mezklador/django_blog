from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=120, verbose_name="rubrique")
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name_plural = "rubriques"
        verbose_name = "rubrique"

def upload_policy(instance, filename):
    """
    Avoiding None in the folder's name if
    it's the first post here...
    """
    the_id = instance.id
    if the_id is None:
        the_id = 1
    return "posts/{}/{}".format(the_id, filename)


class PostManager(models.Manager):
    """
    Re-define DB calls behaviors, such as:
    all(), filter(), etc.
    """
    def active(self, *args, **kwargs):
        """
        In this case: filter DRAFT + Less Than Or Equal now()
        """
        return super(PostManager, self).filter(draft=False).filter(published_at__lte=timezone.now())

class Post(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    ## Get as Foreign Key the Auth Module of Django and set it with
    ## the first user inside its db (superuser, from the get-go)
    title = models.CharField(max_length=120, verbose_name="titre")
    content = models.TextField(verbose_name="contenu")
    picture = models.ImageField(blank=True,
                                null=True,
                                verbose_name='image',
                                width_field="width_field",
                                height_field="height_field",
                                upload_to=upload_policy)
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    slug = models.SlugField(unique=True)
    draft = models.BooleanField(default=False,
                                verbose_name="brouillon")
    published_at = models.DateField(auto_now=False,
                                    auto_now_add=False,
                                    verbose_name="date de publication")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    categories = models.ManyToManyField(Category)

    # Link PostManager to the based-model
    ## CONVENTION: "objects" is the way this instance is called
    ## in views.py -> Post.objects.all(), for eg.
    objects = PostManager()

    def __str__(self):
        return self.title

    """
    dynamic/automagical method to get
    each url link (on loop)

    """
    def get_absolute_url(self):
        #posts:post_detail
        #this call is defined by the namespace inside
        #the include(), in parent > urls.py
        return reverse("post_detail",
                       kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_at', '-updated_at']

# Signal managment to generate slug in Model
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


def create_slug(instance, new_slug=None):
    """ Recursive function, in case of repetitive process """
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        """
        Auto-incrementing id value in the slug's name
        """
        the_id = int(qs.first().id) + 1
        the_new_slug = "{}-{}".format(slug, str(the_id))
        return create_slug(instance, new_slug=the_new_slug)

    return slug

pre_save.connect(pre_save_post_receiver, Post)
pre_save.connect(pre_save_post_receiver, Category)
