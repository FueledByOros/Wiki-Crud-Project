import random
import json
import difflib

from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from wiki.forms import ArticleForm
from .models import Article
from . import utils

from django.db.models import Q


def home(request):
    articles = Article.objects.all()

    return render(request, 'wiki/homepage.html', {
        'articles': articles
    })

def create(request):
    articles = Article.objects.all()
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.title_html = utils.markdown_to_html(form.cleaned_data['title'])
            article.content_html = utils.markdown_to_html(form.cleaned_data['content'])
            article.save()
            return redirect('read', article_id=article.id)
        
    else:
        form = ArticleForm()
    
    return render(request, 'wiki/create.html', {
        'form': form, 
        'errors': form.errors
    })

def search(request):
    articles = Article.objects.all()
    query = request.GET.get("q", "").strip()
    results = Article.objects.none()

    if query:
        all_articles = Article.objects.all()
        
        for article in all_articles:
            plain_title = article.title.lstrip('# ').strip()
            if plain_title.lower() == query.lower():
                return redirect('read', article_id=article.id)
        
        results = list(Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ))
    
    if not results and query:
        return render(request, "wiki/errors.html", {
            "query": query,
        })

    return render(request, "wiki/search.html", {
        "query": query,
        "results": results,
    })

def read(request, article_id):
    articles = Article.objects.all()
    article = get_object_or_404(Article, id=article_id)
    return render(request, "wiki/read.html", {
        "article": article,
    })

def edit(request, article_id):
    articles = Article.objects.all()
    recent_articles = [a for a in articles if utils.recent_check(a) == False]
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.title_html = utils.markdown_to_html(form.cleaned_data['title'])
            article.content_html = utils.markdown_to_html(form.cleaned_data['content'])
            article.save()
            return redirect("read", article_id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, "wiki/edit.html", {
        "form": form,
        "article": article,
        "recent_articles": recent_articles
    })

def delete(request, article_id):
    articles = Article.objects.all()
    article = get_object_or_404(Article, id= article_id)

    if request.method == 'POST':
        article.delete()
        return redirect('home')
    
    return redirect('read', article_id=article.id)

def random_article(request):
    articles = list(Article.objects.all())
    random_article = random.choice(articles)
    return redirect('read', article_id=random_article.id)

def error_404(request, exception):
    articles = Article.objects.all()
    recent_articles = [a for a in articles if utils.recent_check(a)]
    
    return render(request, 'wiki/errors.html', {
        'query': 'Page not found',
        'recent_articles': recent_articles
    }, status=404)
