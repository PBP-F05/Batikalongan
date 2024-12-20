from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .decorators import admin_required
import json
import os
import base64
from batikalongan.settings import MEDIA_ROOT
import time


def home(request):
    return HttpResponse("Hello, welcome to Batik Pekalongan!")

# View to list articles
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

# View to add new articles
@admin_required
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

@admin_required
def add_article_fullscreen(request):
    # Sama seperti add_article, tapi menggunakan template fullscreen
    form = ArticleForm()
    return render(request, 'add_article_fullscreen.html', {'form': form})


# View for individual article
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_detail.html', {'article': article})

@admin_required
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

@admin_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('article:article_list')  # Redirect to the article list after deletion

def show_json(request):
    articles = Article.objects.all()

    articles_data = []

    for article in articles:
        article_data = {
            'id': article.id,
            'title': article.title,
            'introduction': article.introduction,
            'content': article.content,
        }

        if article.image:
            image_path = article.image.path
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
                    article_data['image'] = encoded_image
            else:
                article_data['image'] = None
        else:
            article_data['image'] = None

        articles_data.append(article_data)

    return JsonResponse({'articles': articles_data})

@csrf_exempt
def create_article_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            title = data.get("title")
            introduction = data.get("introduction")
            content = data.get("content")

            image_path = None
            if "image" in data:
                image_data = data.get("image")
                
                image_bytes = base64.b64decode(image_data)

                filename = f"article_{title.replace(' ', '_')}_{int(time.time())}.jpg"
                image_path = os.path.join(MEDIA_ROOT, "articles", filename)

                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                image_path = f"articles/{filename}"

            # Create the new article
            new_article = Article.objects.create(
                title=title,
                introduction=introduction,
                content=content,
                image=image_path
            )

            new_article.save()

            return JsonResponse({"status": "success", "message": "Article created successfully"}, status=200)
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def update_article_flutter(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            article_id = data.get("id")

            article = get_object_or_404(Article, id=article_id)

            article.title = data.get("title", article.title)
            article.introduction = data.get("introduction", article.introduction)
            article.content = data.get("content", article.content)

            if "image" in data and data.get("image"):
                image_data = data.get("image")

                image_bytes = base64.b64decode(image_data)

                filename = f"article_{article.id}.jpg"
                image_path = os.path.join(MEDIA_ROOT, "articles", filename)

                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                article.image = f"articles/{filename}"

            article.save()

            return JsonResponse({"status": "success", "message": "Article updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
@csrf_exempt
def delete_article_flutter(request, id):
    if request.method == 'DELETE':
        try:
            article = get_object_or_404(Article, id=id)
            article.delete()

            return JsonResponse({"status": "success", "message": "Article deleted successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)