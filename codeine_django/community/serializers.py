from rest_framework import serializers

from .models import Article, ArticleComment


class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = '__all__'
    # end Meta
# end class


class ArticleSerializer(serializers.ModelSerializer):
    article_comments = ArticleCommentSerializer(many=True)

    class Meta:
        model = Article
        fields = '__all__'
    # end Meta
# end class
