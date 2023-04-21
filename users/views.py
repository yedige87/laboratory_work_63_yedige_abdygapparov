from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.forms import BaseModelForm
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, UpdateView, CreateView, FormView
from django.urls import reverse

from posts.models import Post
from .forms import CustomUserCreationForm, LoginForm, UserChangeForm, CustomUserChangePasswordForm
from .models import GenderChoice, CustomUser


class RegisterCustomUserView(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        print('request=', request)
        print('kwargs=', kwargs)
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            account = form.save()
            account.username = None
            account.save()
            login(request, account)
            return redirect(self.success_url)
        context = {'form': form}
        return self.render_to_response(context)

class ChangeCustomUserPasswordView(FormView):
    template_name = 'change_password.html'
    form_class = CustomUserChangePasswordForm
#    success_url = '/'

    def post(self, request, *args, **kwargs):
        curr_user = get_object_or_404(CustomUser, pk=self.kwargs.get('pk'))
        form = self.get_form_class()(request.POST, instance=curr_user)
        if form.is_valid():
            curr_user = form.save()
            curr_user.username = None
            curr_user.save()
            login(request, curr_user)
        return redirect('profile', pk=curr_user.pk)

class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, "Некорректные данные")
            return redirect('home')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.warning(request, "Пользователь не найден")
            return redirect('home')
        login(request, user)
        messages.success(request, 'Добро пожаловать, ' + user.full_name + ' !')
        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def get(self, request, *args, **kwargs):
        print('Profile kwargs=', kwargs)
        id = kwargs['pk']
        CustUser = get_user_model()
        prof_user = CustUser.objects.get(pk=id)
        self.extra_context = {'prof_user': prof_user, 'choices': GenderChoice.choices}
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


def subscribe_view(request, pk):
    print('request=', request)
    print('pk=', pk)
    CustUser = get_user_model()
    author = CustUser.objects.get(pk=pk)
    print('на кого подписаться - ', author.full_name)
    # curr_user = CurrUser.curr_user

    curr_user = request.user
    print("кто подписывается - ", curr_user.full_name)
    if not curr_user:
        messages.warning(request, "Вы не авторизованы !")
        return redirect('home')
    curr_user.subscriptions.add(author)
    curr_user.save()
    return redirect(reverse('profile', kwargs={'pk': author.pk}))

def unsubscribe_view(request, pk):
    print('request=', request)
    print('pk=', pk)
    CustUser = get_user_model()
    author = CustUser.objects.get(pk=pk)
    print('на кого подписаться - ', author.full_name)
    # curr_user = CurrUser.curr_user

    curr_user = request.user
    print("кто подписывается - ", curr_user.full_name)
    if not curr_user:
        messages.warning(request, "Вы не авторизованы !")
        return redirect('home')
    curr_user.subscriptions.remove(author)
    curr_user.save()
    return redirect(reverse('profile', kwargs={'pk': author.pk}))


def make_like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    curr_user = request.user
    if not curr_user:
        messages.warning(request, "Вы не авторизованы !")
        return redirect('home')
    if curr_user in post.user_likes.all():
        messages.warning(request, "Вы уже оценили данную публикацию !")
        return redirect('home')
    post.user_likes.add(curr_user)
    post.save()
    return redirect('home')

class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})