from django.urls import path
from posts.views import CommentAddView, PostDetailView, post_check, PostUpdateView, PostDeleteView, create_blank

urlpatterns = [
    path('comment_add/<int:pk>', CommentAddView.as_view(), name='comment_add'),
    path('post/<int:pk>/view/', PostDetailView.as_view(), name='post_detail'),
    path('post/add/', create_blank, name='post_add'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/check/', post_check, name='post_check'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/confirm_delete/', PostDeleteView.as_view(), name='confirm_delete'),
]