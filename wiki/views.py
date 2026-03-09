import random
import json
import difflib

from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Value
from django.db.models.functions import Replace

from django.views.decorators.csrf import csrf_exempt

from wiki.forms import ArticleForm
from .models import Article
from . import utils


def home(request):
    print("[DEBUG] home view called")
    articles = Article.objects.all()
    print(f"[DEBUG] number of articles: {articles.count()}")

    return render(request, 'wiki/homepage.html', {
        'articles': articles
    })


def create(request):
    print("[DEBUG] create view called")
    articles = Article.objects.all()
    print(f"[DEBUG] number of articles: {articles.count()}")

    if request.method == 'POST':
        print("[DEBUG] POST request received in create")
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.title_html = utils.markdown_to_html(form.cleaned_data['title'])
            article.content_html = utils.markdown_to_html(form.cleaned_data['content'])
            article.save()
            print(f"[DEBUG] Article created: {article.id} - {article.title}")
            return redirect('read', article_id=article.id)
        else:
            print(f"[DEBUG] Form errors: {form.errors}")
    else:
        print("[DEBUG] GET request received in create")
        form = ArticleForm()

    return render(request, 'wiki/create.html', {
        'form': form,
        'errors': form.errors
    })


@csrf_exempt
def search(request):
    print("[DEBUG] search view called")
    query = request.GET.get("q", "").strip()
    print(f"[DEBUG] query: '{query}'")
    results = []

    if query:
        normalized_query = query.replace(' ', '').replace('#', '').lower()

        all_articles = Article.objects.all()

        # Exact title match → redirect directly
        for article in all_articles:
            normalized_title = article.title.replace(' ', '').replace('#', '').lower()
            if normalized_title == normalized_query:
                return redirect('read', article_id=article.id)

        # Partial match on title or content
        for article in all_articles:
            normalized_title = article.title.replace(' ', '').replace('#', '').lower()
            normalized_content = article.content.replace(' ', '').lower()
            if normalized_query in normalized_title or normalized_query in normalized_content:
                results.append(article)

    return render(request, "wiki/search.html", {
        "query": query,
        "results": results,
    })


def read(request, article_id):
    print(f"[DEBUG] read view called with article_id={article_id}")
    article = get_object_or_404(Article, id=article_id)
    print(f"[DEBUG] Article retrieved: {article.title}")
    return render(request, "wiki/read.html", {
        "article": article,
    })


def edit(request, article_id):
    print(f"[DEBUG] edit view called with article_id={article_id}")
    articles = Article.objects.all()
    recent_articles = [a for a in articles if utils.recent_check(a) == False]
    article = get_object_or_404(Article, id=article_id)
    print(f"[DEBUG] Article to edit: {article.title}")

    if request.method == "POST":
        print("[DEBUG] POST request received in edit")
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.title_html = utils.markdown_to_html(form.cleaned_data['title'])
            article.content_html = utils.markdown_to_html(form.cleaned_data['content'])
            article.save()
            print(f"[DEBUG] Article updated: {article.id} - {article.title}")
            return redirect("read", article_id=article.id)
        else:
            print(f"[DEBUG] Form errors: {form.errors}")
    else:
        print("[DEBUG] GET request received in edit")
        form = ArticleForm(instance=article)

    return render(request, "wiki/edit.html", {
        "form": form,
        "article": article,
        "recent_articles": recent_articles
    })


def delete(request, article_id):
    print(f"[DEBUG] delete view called with article_id={article_id}")
    articles = Article.objects.all()
    article = get_object_or_404(Article, id=article_id)
    print(f"[DEBUG] Article to delete: {article.title}")

    if request.method == 'POST':
        print("[DEBUG] POST request received in delete")
        article.delete()
        print(f"[DEBUG] Article deleted: {article_id}")
        return redirect('home')

    return redirect('read', article_id=article.id)


def random_article(request):
    print("[DEBUG] random_article view called")
    articles = list(Article.objects.all())
    random_article = random.choice(articles)
    print(f"[DEBUG] Random article chosen: {random_article.id} - {random_article.title}")
    return redirect('read', article_id=random_article.id)


def error_404(request, exception):
    print("[DEBUG] error_404 view called")
    articles = Article.objects.all()
    recent_articles = [a for a in articles if utils.recent_check(a)]
    return render(request, 'wiki/errors.html', {
        'query': 'Page not found',
        'recent_articles': recent_articles
    }, status=404)