from django.urls import path

from . import views_article, views_article_comments, views_engagement

urlpatterns = [
    # article views
    path('', views_article.article_view, name='Create/Get all/Search Articles'),
    path('/<slug:pk>', views_article.single_article_view, name='Read/update/delete for Articles'),

    # article comment views
    path('/<slug:article_id>/comments', views_article_comments.article_comment_view, name='Create/Get all/Search Article Comments'),
    path('/<slug:article_id>/comments/<slug:pk>', views_article_comments.single_article_comment_view, name='Read/update/delete for Article Comments'),

    # engagement views
    path('/<slug:article_id>/engagement', views_engagement.engagement_view, name='Create/Get all/Search Engagements'),
    path('/<slug:article_id>/engagement/<slug:pk>', views_engagement.single_engagement_view, name='Read/update/delete for Engagements'),
]
