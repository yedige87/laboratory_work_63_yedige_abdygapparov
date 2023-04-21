import django
from django.template.defaulttags import url
from django.urls import path

from .views import ProfileView, subscribe_view, LoginView, make_like_view, UserChangeView, unsubscribe_view, \
    RegisterCustomUserView, ChangeCustomUserPasswordView



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path("signup/", RegisterCustomUserView.as_view(), name="signup"),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('change_password/<int:pk>', ChangeCustomUserPasswordView.as_view(), name='change_password'),
    path('subsribe/<int:pk>', subscribe_view, name='subsribe'),
    path('unsubsribe/<int:pk>', unsubscribe_view, name='unsubsribe'),
    path('make_like/<int:pk>', make_like_view, name='make_like'),
    path('profile/<int:pk>/change', UserChangeView.as_view(), name='user_change'),
]