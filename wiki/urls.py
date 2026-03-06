from django.urls import path

from . import views, api_views

urlpatterns = [
    # Web page routes
    path('home/', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('read/<int:article_id>/', views.read, name='read'),
    path('search/', views.search, name='search'),
    path('edit/<int:article_id>/', views.edit, name='edit'),
    path('delete/<int:article_id>/', views.delete, name='delete'),
    path('random_article/', views.random_article, name='random_article'),
    # API endpoints
    path('api/articles/<int:article_id>/', api_views.api_article, name='api_article'),
    path('api/articles/', api_views.api_all_articles, name='api_all_articles'),
    path('api/articles/create/', api_views.api_create_article, name='api_create_article'),
    path('api/articles/<int:article_id>/edit/', api_views.api_update_article, name='api_update_article'),
    path('api/articles/<int:article_id>/delete/', api_views.api_delete_article, name='api_delete_article'),
    ]

