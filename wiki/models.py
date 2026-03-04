from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    title_html = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    content_html = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
