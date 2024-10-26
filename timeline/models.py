import uuid
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
   id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
   title = models.CharField(max_length = 500)
   artist = models.CharField(max_length=500, null=True)
   url = models.URLField(max_length=500, null=True)
   image = models.URLField(max_length= 500)
   author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
   body = models.TextField()
   created = models.DateTimeField(auto_now_add=True)
   likes = models.ManyToManyField(User, related_name="likedposts", through="LikedPost")
   files = models.FileField(null=True, blank=True, upload_to='file_uploads/')


   def __str__(self):
      return str(self.title)

   class Meta:
      ordering = ['-created']

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}' 
        except:
            return f'no author : {self.body[:30]}' 
        
    class Meta:
        ordering = ['-created']

class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="replies")
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedreplies', through='LikedReply')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'

    class Meta:
        ordering = ['created']

class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.post.title}'

class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'

class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.reply.body[:30]}'