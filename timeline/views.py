from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import *
from.forms import *
from django.contrib import messages
from bs4 import BeautifulSoup
import requests

def home_view(request):
   posts = Post.objects.all()
   return render(request, 'posts/home.html', {'posts' : posts})

def post_create_view(request):
   if request.method == 'POST':
      form = PostCreateForm(request.POST, request.FILES)
      if form.is_valid():
         post = form.save(commit=False)
         post.author = request.user
         post.save()
         return redirect('home')

   return render(request, 'posts/post_create.html', {'form' : form })

def post_delete_view(request, pk):
   post = Post.objects.get(id=pk)

   if request.method == 'POST':
      post.delete()
      messages.success(request, 'Post deleted')
      return redirect('home')
      
   return render(request, 'posts/post_delete.html', {'post' : post })

def post_edit_view(request, pk):
   post = Post.objects.get(id=pk)
   form = PostEditForm(instance=post)

   if request.method == 'POST':
      form = PostEditForm(request.POST, instance=post)
      if form.is_valid:
         form.save()
         messages.success(request, 'Post updated' )
         return redirect('home')
   
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
         return redirect('post', post.id)
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
      return redirect('post', post.parent_post.id)
      
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

   return redirect('post', comment.parent_post.id)

def reply_delete_view(request, pk):
   reply = get_object_or_404(Reply, id=pk, author=request.user)

   if request.method == 'POST':
      reply.delete()
      messages.success(request, 'Reply deleted')
      return redirect('post', reply.parent_comment.parent_post.id)
      
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