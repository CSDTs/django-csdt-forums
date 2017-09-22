from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.views import generic
from ttp import ttp

from . import forms
from . import models
from posts.models import Post


User = get_user_model()


class AllPosts(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "community")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_timeline.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
            person = User.objects.get(username=self.kwargs.get("username"))
            posts = Post.objects.filter(Q(user=person) | Q(atted=person))
        except User.DoesNotExist:
            raise Http404
        else:
            return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class SinglePost(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "community")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, generic.CreateView):
    form_class = forms.PostForm
    model = models.Post

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "community")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def get_object(self, queryset=None):
        if self.request.user.is_superuser:
            pk = self.kwargs.get(self.pk_url_kwarg, None)
            queryset = models.Post.objects.filter(pk=pk)
            try:
                obj = queryset.get()
            except models.Post.ObjectDoesNotExist:
                raise Http404(_(u"No %(verbose_name)s found matching the query") %
                              {'verbose_name': queryset.model._meta.verbose_name})
            return obj
        else:
            pk = self.kwargs.get(self.pk_url_kwarg, None)
            try:
                queryset = models.Post.objects.filter(user_id=self.request.user.id,pk=pk)
            except models.Post.ObjectDoesNotExist:
                raise Http404(_(u"Not a mod, can't delete other's posts"))
            else:
                try:
                    obj = queryset.get()
                except models.Post.ObjectDoesNotExist:
                    raise Http404(_(u"No %(verbose_name)s found matching the query") %
                                  {'verbose_name': queryset.model._meta.verbose_name})
                return obj

    def delete(self, *args, **kwargs):
        if self.request.user.is_superuser:
            self.object = self.get_object()
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())

        messages.success(self.request, "Message successfully deleted")
        return super().delete(*args, **kwargs)

class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("posts:all")
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


# class SignUp(generic.CreateView):
#     form_class = forms.UserCreateForm
#     success_url = reverse_lazy("login")
#     template_name = "accounts/signup.html"
