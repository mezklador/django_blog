## FROM: https://www.google.fr/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwj865z7_NjPAhWG1BoKHQWAA3cQFggeMAA&url=https%3A%2F%2Frayed.com%2Fwordpress%2F%3Fp%3D1266&usg=AFQjCNFXle-ogxFeIBcyckrI43iWG_WCDw&sig2=IqlRRiidHTBeE-b3wpRmXQ
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (ListView,
                                  DetailView)
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)

from .forms import PostForm
from .models import Post


class BlogListView(ListView):
    """
    CHECK: http://www.robgolding.com/blog/2012/11/17/django-class-based-view-mixins-part-2/
    Sorting technique in CBV on queryset, based on request (GET)
    HERE: sorting by "updated_at" datetime, from recent to old (DESC)

    NOT HERE! -> just add class Meta to Model and added ordering kwarg.
    """
    model = Post
    context_object_name = 'all_posts'
    # sorted_field = 'created_at'
    """
    FROM: http://stackoverflow.com/questions/5907575/how-do-i-use-pagination-with-django-class-based-generic-listviews#answer-33485595
    HERE: pagination active and set to 2 articles per pages
    """
    paginate_by = 2

    def get_queryset(self):
        """
        Prevent listview for anonymous users to check Drafts & Future Posts
        """
        querylist = Post.objects.active()
        if self.request.user.is_staff or self.request.user.is_superuser:
            querylist = Post.objects.all()

        # Query Search from front page (GET => "s")
        search_query = self.request.GET.get("s")
        if search_query:
            return querylist.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(writer__first_name__icontains=search_query) |
                Q(writer__last_name__icontains=search_query) |
                Q(writer__username__icontains=search_query)
            ).distinct()

        return querylist


class BlogDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        """ Limited access to data where there are not defined as DRAFT """
        context = super(BlogDetailView, self).get_context_data(*args, **kwargs)
        obj = context['object']  # This is the way to get a property from the model
        if obj.draft or obj.published_at > timezone.now().date():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise Http404
        return context


"""
form_class: DRY declaration to avoid
            repeating fields' attributes, like:
            - fields
 """


class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog_list')
    # flash messages management: SUCCESS
    success_message = ""

    # fields = ['title', 'content', 'picture']

    def get_context_data(self, **kwargs):
        """ Adding 'birth' key in context for template adjustments """
        context = super(BlogCreateView, self).get_context_data(**kwargs)
        context['birth'] = True
        context['bouton'] = "Créer"
        return context

    def form_valid(self, form):
        """
        A better way to handle flash messages
        without encoding error + HTML tags
        BEWARE: check how to get property
        from form instance (and not self.object)
        """
        self.success_message = "L'article <strong>{}</strong> sauvegardé avec succès.".format(
            form.cleaned_data['title'])
        return super(BlogCreateView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BlogCreateView, self).dispatch(*args, **kwargs)


class BlogUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog_list')
    # fields = ['title', 'content', 'picture']
    # flash messages management: SUCCESS
    success_message = ""

    def get_context_data(self, **kwargs):
        """ Adding 'birth' key in context for template adjustments """
        context = super(BlogUpdateView, self).get_context_data(**kwargs)
        context['birth'] = False
        context['bouton'] = "Actualiser"
        return context

    def form_valid(self, form):
        """
        A better way to handle flash messages
        without encoding error + HTML tags
        BEWARE: not the same property as createview
        """
        self.success_message = "L'article <strong>{}</strong> a été modifié avec succès.".format(self.object.title)
        return super(BlogUpdateView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BlogUpdateView, self).dispatch(*args, **kwargs)


class BlogDeleteView(SuccessMessageMixin, DeleteView):
    model = Post
    success_message = "L'article %(title) a été supprimé"
    success_url = reverse_lazy('blog_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BlogCreateView, self).dispatch(*args, **kwargs)
