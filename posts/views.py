from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import FormView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from posts.forms import CommentForm, SearchForm, PostForm
from posts.models import Comment, Post


# Create your views here.


class HomeView(ListView):
    template_name = "home.html"
    model = Post
    context_object_name = 'posts'
    ordering = ('-date_update',)
    extra_context = {"comments": Comment.objects.all()}

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):

        queryset = super().get_queryset().all()  # .exclude(is_deleted=True)
        if self.search_value:
            query = Q(author__full_name__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        context['comment_form'] = CommentForm()
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class CommentAddView(LoginRequiredMixin, FormView):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            if text:
                curr_user = request.user
                comment = Comment()
                comment.post = post
                comment.text = text
                comment.author = curr_user
                comment.save()
                messages.success(request, 'Комментарий к посту добавлен!')
            else:
                messages.warning(request, 'Комментарий к посту не добавлен!')
        return redirect('home')


class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    model = Post
    extra_context = {'comments': Comment.objects.all()}


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'post_update.html'
    form_class = PostForm
    model = Post
    success_message = 'Пост обновлён!'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('home')
    success_message = 'Пост удалён!'


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    model = Post
    form_class = PostForm
    success_message = 'Пост создан!'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


def create_blank(request: WSGIRequest):
    if request.method == "GET":
        post = Post()
        post.author = request.user
        print(post.image)
        post.save()
        return redirect(reverse('post_update', kwargs={'pk': post.pk}))
    return redirect('home')

def post_check(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.description == '' and post.is_new and ('blank.jpg' in str(post.image)):
        post.delete()
        return redirect('home')
    elif post.is_new and not('blank.jpg' in post.image):
            post.is_new = False
            post.save()
    return redirect(reverse('post_detail', kwargs={'pk': post.pk}))
