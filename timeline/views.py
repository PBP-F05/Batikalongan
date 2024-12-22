from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import *
from.forms import *
from django.contrib import messages
from bs4 import BeautifulSoup
import requests
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, LikedPost
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags

def home_view(request):
   posts = Post.objects.all()
   return render(request, 'posts/home.html', {'posts' : posts})

def post_create_view(request):
    form = PostCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('timeline:home') 
    
    return render(request, 'posts/post_create.html', {'form': form})

def post_delete_view(request, pk):
   post = get_object_or_404(Post, id=pk)
   if request.method == 'POST':
      post.delete()
      messages.success(request, 'Post deleted')
      return redirect('timeline:home')
      
   return render(request, 'posts/post_delete.html', {'post' : post })

def post_edit_view(request, pk):
   post = Post.objects.get(id=pk)
   form = PostEditForm(instance=post)

   if request.method == 'POST':
      form = PostEditForm(request.POST, instance=post)
      if form.is_valid:
         form.save()
         messages.success(request, 'Post updated' )
         return redirect('timeline:home')
   
   context = {
      'post' : post,
      'form' : form,
   }
   return render(request, 'posts/post_edit.html', context)

def post_page_view(request, pk):
   post = get_object_or_404(Post, id=pk)
   commentform = CommentCreateForm()
   replyform = ReplyCreateForm()

   context = {
      'post' : post,
      'commentform' : commentform,
      'replyform' : replyform,
   }

   return render(request, 'posts/post_page.html', context)


def comment_sent(request, pk):
   # post = Post.objects.get(id=pk)
   post = get_object_or_404(Post, id=pk)
   #  replyform = ReplyCreateForm()
    
   if request.method == 'POST':
      form = CommentCreateForm(request.POST)
      if form.is_valid():
         comment = form.save(commit=False)
         comment.author = request.user
         comment.parent_post = post            
         comment.save()
         return redirect('timeline:post', post.id)
      else:
         print(form.errors)

   return redirect('post', post.id)
   #  context = {
   #      'post' : post,
   #      'comment': comment,
   #      'replyform': replyform
   #  }

   #  return render(request, 'snippets/add_comment.html', context)

def comment_delete_view(request, pk):
   post = get_object_or_404(Comment, id=pk, author=request.user)

   if request.method == 'POST':
      post.delete()
      messages.success(request, 'Comment deleted')
      return redirect('timeline:post', post.parent_post.id)
      
   return render(request, 'posts/comment_delete.html', {'comment' : post })


def reply_sent(request, pk):
   comment = get_object_or_404(Comment, id=pk)
    
   if request.method == 'POST':
      form = ReplyCreateForm(request.POST)
      if form.is_valid():
         reply = form.save(commit=False)
         reply.author = request.user
         reply.parent_comment = comment           
         reply.save()

   return redirect('timeline:post', comment.parent_post.id)

def reply_delete_view(request, pk):
   reply = get_object_or_404(Reply, id=pk, author=request.user)

   if request.method == 'POST':
      reply.delete()
      messages.success(request, 'Reply deleted')
      return redirect('timeline:post', reply.parent_comment.parent_post.id)
      
   return render(request, 'posts/reply_delete.html', {'reply' : reply })

def like_post(request, pk):
   post = get_object_or_404(Post, id=pk)
   user_exist = post.likes.filter(username=request.user.username).exists()

   if post.author != request.user:
      if user_exist:
         post.likes.remove(request.user)
      else:
         post.likes.add(request.user)
   
   return render(request,'snip/likes.html',{'post': post})

def like_comment(request, pk):
   comment = get_object_or_404(Comment, id=pk)
   user_exist = comment.likes.filter(username=request.user.username).exists()

   if comment.author != request.user:
      if user_exist:
         comment.likes.remove(request.user)
      else:
         comment.likes.add(request.user)
   
   return render(request,'snip/likes_comment.html',{'comment': comment})

def like_reply(request, pk):
   reply = get_object_or_404(Reply, id=pk)
   user_exist = reply.likes.filter(username=request.user.username).exists()

   if reply.author != request.user:
      if user_exist:
         reply.likes.remove(request.user)
      else:
         reply.likes.add(request.user)
   
   return render(request,'snip/likes_reply.html',{'reply': reply})


   #  def inner_func(func):
   #      def wrapper(request, *args, **kwargs):
            
                    
   #          return func(request, post)
   #      return wrapper
   #  return inner_func

def home_view_json(request):
    user = request.user if request.user.is_authenticated else None
    posts = Post.objects.prefetch_related('likes', 'comments__replies')  # Prefetch related data for efficiency

    posts_json = [
        {
            "id": post.id,
            "author": post.author.username if post.author else None,
            "body": post.body,
            "created": post.created.isoformat(),
            "is_liked_by_user": post.likes.filter(id=user.id).exists() if user else False,
            "like_count": post.likes.count(),
            "comment_count": post.comments.count(),
            "comments": [
                {
                    "id": comment.id,
                    "author": comment.author.username if comment.author else None,
                    "body": comment.body,
                    "created": comment.created.isoformat(),
                }
                for comment in post.comments.all()
            ],
        }
        for post in posts
    ]

    return JsonResponse(posts_json, safe=False)

@csrf_exempt
def toggle_like(request):
    # Parse the incoming JSON request body
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        
        # Ensure post_id is provided
        if not post_id:
            return JsonResponse({'message': 'Post ID is required'}, status=400)

        # Get the post object
        post = Post.objects.get(id=post_id)

        # Check if the user has already liked this post
        existing_like = LikedPost.objects.filter(post=post, user=request.user).first()

        if existing_like:
            # If the user has already liked the post, remove the like
            existing_like.delete()
            message = "Like removed"
        else:
            # If the user hasn't liked the post, add a like
            LikedPost.objects.create(post=post, user=request.user)
            message = "Post liked"

        # Return a JSON response with the message
        return JsonResponse({'message': message})

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'Post not found'}, status=404)

@csrf_exempt  # To disable CSRF validation (use only if necessary)
def delete_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            
            post = Post.objects.get(id=post_id)
            post.delete()
            
            return JsonResponse({'message': 'Post deleted'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'Post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
        
@csrf_exempt 
def delete_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_id = data.get('comment_id')
            
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            
            return JsonResponse({'message': 'Comment deleted'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'Comment not found'}, status=404)
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def create_post(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_mood = Post.objects.create(
            author=request.user,
            body=data["body"]
        )

        new_mood.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def create_comment(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_mood = Comment.objects.create(
            author=request.user,
            body=data["body"],
            parent_post=Post.objects.get(id=data['parent_post_id'])
        )

        new_mood.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)