from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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
            article = form.save()
            # Response for AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'title': article.title,
                    'introduction': article.introduction,
                    'image_url': article.image.url if article.image else '',
                    'id': article.id,
                })
            return redirect('article:article_list')
        else:
            # Send form errors if form is not valid
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = ArticleForm()

    return render(request, 'add_article.html', {'form': form})

def add_article_fullscreen(request):
    # Sama seperti add_article, tapi menggunakan template fullscreen
    form = ArticleForm()
    return render(request, 'add_article_fullscreen.html', {'form': form})


# View for individual article
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_detail.html', {'article': article})

def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)  # Include request.FILES
        if form.is_valid():
            form.save()
            next_page = request.GET.get('next', 'article:article_list')  # Default to article_list
            if next_page == 'article:article_list':
                return redirect('article:article_list')  # Redirect to article_list
            else:
                return redirect('article:article_detail', id=article.id)  # Redirect to detail page
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'edit_article.html', {'form': form})


def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('article:article_list')  # Redirect to the article list after deletion

