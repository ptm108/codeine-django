from rest_framework import serializers

from .models import Article, ArticleComment


class ArticleCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleComment
        fields = '__all__'
    # end Meta
# end class


class ArticleSerializer(serializers.ModelSerializer):
    top_level_comments = serializers.SerializerMethodField('get_top_level_comments')

    class Meta:
        model = Article
        fields = '__all__'
    # end Meta

    def get_top_level_comments(self, obj):
        top_level_comments = ArticleComment.objects.filter(parent_comment=None, article=obj)
        return ArticleCommentSerializer(top_level_comments, many=True).data
    # end def
# end class
