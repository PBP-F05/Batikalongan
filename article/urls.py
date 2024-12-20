from django.urls import path
from article.views import home, article_list, add_article, add_article_fullscreen, article_detail, edit_article, delete_article, show_json, create_article_flutter, update_article_flutter, delete_article_flutter
from django.conf import settings
from django.conf.urls.static import static

app_name = 'article'

urlpatterns = [
    path('', article_list, name='article_list'),
    path('<int:id>', article_detail, name='article_detail'),
    path('add', add_article, name='add_article'),
    path('add/fullscreen', add_article_fullscreen, name='add_article_fullscreen'),
    path('edit/<int:id>', edit_article, name='edit_article'),
    path('delete/<int:id>', delete_article, name='delete_article'),
    path('json/', show_json, name='show_json'),
    path('create-flutter/', create_article_flutter, name='create_article_flutter'),
    path('update-flutter/', update_article_flutter, name='update_article_flutter'),
    path('delete-flutter/<int:id>', delete_article_flutter, name='delete_article_flutter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)