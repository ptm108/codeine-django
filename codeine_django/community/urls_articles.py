from django.urls import path

from . import views_article, views_article_comments, views_article_engagement

urlpatterns = [
    # article views
    path('', views_article.article_view, name='Create/Get all/Search Articles'),
    path('/<slug:pk>', views_article.single_article_view,
         name='Read/update/delete for Articles'),
    path('/user/', views_article.user_article_view,
         name='Get user\'s Article'),
    path('/<slug:pk>/publish', views_article.publish_article_view,
         name='user publish Article'),
    path('/<slug:pk>/unpublish', views_article.unpublish_article_view,
         name='user unpublish Article'),
    path('/<slug:pk>/engagements', views_article.article_engagement_view,
         name='Like/Unlike article'),

    # article comment views
    path('/<slug:article_id>/comments', views_article_comments.article_comment_view,
         name='Create/Get all/Search Article Comments'),
    path('/<slug:article_id>/comments/<slug:pk>', views_article_comments.single_article_comment_view,
         name='Read/update/delete for Article Comments'),
    path('/<slug:article_id>/comments/<slug:pk>/pin', views_article_comments.pin_comment_view,
         name='Pin Article Comments'),
    path('/<slug:article_id>/comments/<slug:pk>/unpin', views_article_comments.unpin_comment_view,
         name='Unpin Article Comments'),
    path('/<slug:article_id>/comments/<slug:pk>/engagements', views_article_comments.article_comment_engagement_view,
         name='Like/Unlike article comments'),

    # article engagement views
#     path('/<slug:article_id>/engagement', views_article_engagement.article_engagement_view,
#          name='Create/Get all/Search Engagements'),
#     path('/<slug:article_id>/engagement/<slug:pk>',
#          views_article_engagement.single_article_engagement_view, name='Read/update/delete for Engagements'),
]
