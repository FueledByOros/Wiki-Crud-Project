from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json

from wiki.models import Article
import datetime

def api_all_articles(request):
    if request.method == 'GET':
        articles = Article.objects.all().values('id', 'title', 'content', 'created_at', 'updated_at')
        return JsonResponse(list(articles), safe=False)


def api_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'created_at': article.created_at,
            'updated_at': article.updated_at
        })
    
@csrf_exempt
def api_create_article(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        
        if not title or not content:
            return JsonResponse({'error': 'Title and content are required'}, status=400)
        
        try:
            article = Article.objects.create(
                title=title,
                content=content
            )
            return JsonResponse({
                'message': 'Article created successfully',
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'created_at': str(article.created_at),
                'updated_at': str(article.updated_at)
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def api_update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            if 'title' in data:
                article.title = data['title']
            if 'content' in data:
                article.content = data['content']
            
            article.save()
            
            return JsonResponse({
                'message': 'Article updated successfully',
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'created_at': str(article.created_at),
                'updated_at': str(article.updated_at)
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def api_delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'DELETE':
        article.delete()
        return JsonResponse({'message': 'Article deleted successfully'}, status=204)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
