from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    introduction = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title
