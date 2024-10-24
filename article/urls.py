from django.urls import path
from article.views import home, article_list, add_article, article_detail, edit_article, delete_article
from django.conf import settings
from django.conf.urls.static import static

app_name = 'article'

urlpatterns = [
    path('', home, name='home'),
    path('article/', article_list, name='article_list'),
    path('article/<int:id>/', article_detail, name='article_detail'),
    path('article/add/', add_article, name='add_article'),
    path('article/<int:id>/', article_detail, name='article_detail'), 
    path('article/edit/<int:id>/', edit_article, name='edit_article'),
    path('article/delete/<int:id>/', delete_article, name='delete_article'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)