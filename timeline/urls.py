from django.urls import path
from timeline.views import *

app_name = 'timeline'

urlpatterns = [
    path('', home_view, name='home'),
    path('post/create/', post_create_view, name='post-create'),
    path('post/delete/<pk>/', post_delete_view, name='post-delete'),
    path('post/edit/<pk>/', post_edit_view, name='post-edit'),
    path('post/<pk>/', post_page_view, name='post'),
    path('post/like/<pk>/', like_post, name='like-post'),
    path('commentsent/<pk>/', comment_sent, name='comment-sent'),
    path('comment/delete/<pk>/', comment_delete_view, name='comment-delete'),
    path('comment/like/<pk>/', like_comment, name='like-comment'),
    path('reply-sent/<pk>/', reply_sent, name='reply-sent'),
    path('reply/delete/<pk>/', reply_delete_view, name='reply-delete'),
    path('reply/like/<pk>/', like_reply, name='like-reply'),
]
