from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

user= get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.id})
    

