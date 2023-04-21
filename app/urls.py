from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import PostViewSet
from posts.views import HomeView

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("api/views/", include(router.urls)),
    path("users/", include("users.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path("posts/", include("posts.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

