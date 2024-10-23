from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponse
from django.urls import reverse

def home(request):
    return HttpResponse("Hello, welcome to Batik Pekalongan!")

# View to list articles
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

# View to add new articles
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article:article_list')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})

# View for individual article
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_detail.html', {'article': article})

def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            # Ambil parameter 'next' dari query string
            next_page = request.GET.get('next', 'article:article_list')  # Default ke article_list jika tidak ada
            if next_page == 'article:article_list':
                return redirect('article:article_list')  # Redirect ke article_list tanpa query string
            else:
                return redirect('article:article_detail', id=article.id)  # Redirect ke detail artikel
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form})


def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('article:article_list')  # Redirect to the article list after deletion

