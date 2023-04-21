
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.serializers import PostSerializer
from posts.models import Post


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer