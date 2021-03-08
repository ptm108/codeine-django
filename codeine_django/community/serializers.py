from rest_framework import serializers

from .models import Article, ArticleComment, Engagement, CodeReview, CodeReviewComment
from common.serializers import NestedBaseUserSerializer


class NestedCodeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReview
        fields = '__all__'
    # end Meta
# end class


class NestedCodeReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReviewComment
        fields = '__all__'
    # end Meta
# end class


class ParentArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ('id')
    # end Meta
# end class


class NestedArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = '__all__'
    # end Meta
# end class


class ParentCodeReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReviewComment
        fields = ('id')
    # end Meta
# end class


class ArticleCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')
    parent_comment = serializers.SerializerMethodField('get_parent_comment')

    class Meta:
        model = ArticleComment
        fields = '__all__'
    # end Meta'

    def get_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.user, context={'request': request}).data
    # end def

    def get_parent_comment(self, obj):
        request = self.context.get("request")
        if obj.parent_comment is None:
            return None
        else:
            return ParentArticleCommentSerializer(obj.parent_comment, context={'request': request}).data
        # end if-else
    # end def

# end class


class CodeReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')
    code_review = NestedCodeReviewSerializer()
    parent_comment = serializers.SerializerMethodField('get_parent_comment')

    class Meta:
        model = CodeReviewComment
        fields = '__all__'
    # end Meta

    def get_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.user, context={'request': request}).data
    # end def

    def get_parent_comment(self, obj):
        request = self.context.get("request")
        if obj.parent_comment is None:
            return None
        else:
            return ParentCodeReviewCommentSerializer(obj.parent_comment, context={'request': request}).data
        # end if-else
    # end def
# end class


class ArticleSerializer(serializers.ModelSerializer):
    top_level_comments = serializers.SerializerMethodField(
        'get_top_level_comments')
    engagements = serializers.SerializerMethodField('get_engagements')

    class Meta:
        model = Article
        fields = '__all__'
    # end Meta

    def get_top_level_comments(self, obj):
        request = self.context.get("request")
        top_level_comments = ArticleComment.objects.filter(
            parent_comment=None, article=obj)
        return ArticleCommentSerializer(top_level_comments, many=True, context={'request': request}).data
    # end def

    def get_engagements(self, obj):
        request = self.context.get("request")
        engagements = Engagement.objects.filter(article=obj)
        return EngagementSerializer(engagements, many=True, context={'request': request}).data
    # end def
# end class


class EngagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Engagement
        fields = '__all__'
    # end Meta
# end class


class CodeReviewSerializer(serializers.ModelSerializer):
    top_level_comments = serializers.SerializerMethodField(
        'get_top_level_comments')
    member = serializers.SerializerMethodField('get_member')

    class Meta:
        model = CodeReview
        fields = '__all__'
    # end Meta

    def get_top_level_comments(self, obj):
        request = self.context.get("request")
        top_level_comments = CodeReviewComment.objects.filter(
            parent_comment=None, code_review=obj)
        return CodeReviewCommentSerializer(top_level_comments, many=True, context={'request': request}).data
    # end def

    def get_member(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
    # end def
# end class
