from rest_framework import serializers

from .models import Article, ArticleComment, ArticleEngagement, CodeReview, CodeReviewComment, ArticleCommentEngagement, CodeReviewEngagement, CodeReviewCommentEngagement
from common.serializers import NestedBaseUserSerializer


class NestedCodeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReview
        fields = '__all__'
    # end Meta
# end class


class ParentCodeReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReviewComment
        fields = ['id']
    # end Meta
# end class


class NestedCodeReviewCommentSerializer(serializers.ModelSerializer):
    user = NestedBaseUserSerializer()
    replies = serializers.SerializerMethodField('get_replies')
    parent_comment = ParentCodeReviewCommentSerializer()
    reply_count = serializers.SerializerMethodField('get_reply_count')
    likes = serializers.SerializerMethodField('get_likes')
    current_user_liked = serializers.SerializerMethodField('get_current_user_liked')

    class Meta:
        model = CodeReviewComment
        fields = '__all__'
    # end Meta

    def get_replies(self, obj):
        request = self.context.get("request")
        if self.context.get("recursive"):
            return NestedCodeReviewCommentSerializer(obj.replies, many=True, context={'request': request}).data
        else:
            return CodeReviewCommentSerializer(obj.replies, many=True, context={'request': request}).data
        # end if else
    # end def

    def get_reply_count(self, obj):
        def rec_reply_count(comment):
            if len(comment.replies.all()) == 0:
                return 1
            else:
                count = 1
                for reply in comment.replies.all():
                    count += rec_reply_count(reply)
                # end for
                return count
            # end if else
        # end def

        return rec_reply_count(obj) - 1 # minus self
    # end def

    def get_likes(self, obj):
        return CodeReviewCommentEngagement.objects.filter(comment=obj).count()
    # end def

    def get_current_user_liked(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return None
        else:
            user = request.user
            return CodeReviewCommentEngagement.objects.filter(comment=obj).filter(user=user).exists()
        # end if-else
    # end def
# end class


class ParentArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['id', 'display_id']
    # end Meta
# end class


class NestedArticleCommentSerializer(serializers.ModelSerializer):
    user = NestedBaseUserSerializer()
    replies = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    reply_to = ParentArticleCommentSerializer()
    reply_count = serializers.SerializerMethodField('get_reply_count')
    current_user_liked = serializers.SerializerMethodField('get_current_user_liked')

    class Meta:
        model = ArticleComment
        fields = '__all__'
    # end Meta

    def get_replies(self, obj):
        request = self.context.get("request")
        if self.context.get("recursive"):
            return NestedArticleCommentSerializer(obj.replies, many=True, context={'request': request}).data
        else:
            return ArticleCommentSerializer(obj.replies, many=True, context={'request': request}).data
        # end if else
    # end def

    def get_likes(self, obj):
        return ArticleCommentEngagement.objects.filter(comment=obj).count()
    # end def

    def get_reply_count(self, obj):
        def rec_reply_count(comment):
            if len(comment.replies.all()) == 0:
                return 1
            else:
                count = 1
                for reply in comment.replies.all():
                    count += rec_reply_count(reply)
                # end for
                return count
            # end if else
        # end def

        return rec_reply_count(obj) - 1 # minus self
    # end def

    def get_current_user_liked(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return None
        else:
            user = request.user
            return ArticleCommentEngagement.objects.filter(comment=obj).filter(user=user).exists()
        # end if-else
    # end def
# end class


class ArticleCommentSerializer(serializers.ModelSerializer):
    user = NestedBaseUserSerializer()
    likes = serializers.SerializerMethodField()
    reply_to = ParentArticleCommentSerializer()
    reply_count = serializers.SerializerMethodField('get_reply_count')
    current_user_liked = serializers.SerializerMethodField('get_current_user_liked')

    class Meta:
        model = ArticleComment
        fields = '__all__'
    # end Meta'

    def get_likes(self, obj):
        return ArticleCommentEngagement.objects.filter(comment=obj).count()
    # end def

    def get_parent_comment(self, obj):
        request = self.context.get("request")
        if obj.parent_comment is None:
            return None
        else:
            return ParentArticleCommentSerializer(obj.parent_comment, context={'request': request}).data
        # end if-else
    # end def

    def get_reply_count(self, obj):
        def rec_reply_count(comment):
            if len(comment.replies.all()) == 0:
                return 1
            else:
                count = 1
                for reply in comment.replies.all():
                    count += rec_reply_count(reply)
                # end for
                return count
            # end if else
        # end def

        return rec_reply_count(obj) - 1 # minus self
    # end def

    def get_current_user_liked(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return None
        else:
            user = request.user
            return ArticleCommentEngagement.objects.filter(comment=obj).filter(user=user).exists()
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
    user = serializers.SerializerMethodField('get_user')
    top_level_comments = serializers.SerializerMethodField(
        'get_top_level_comments')
    engagements = serializers.SerializerMethodField('get_engagements')
    current_user_liked = serializers.SerializerMethodField('get_current_user_liked')

    class Meta:
        model = Article
        fields = '__all__'
    # end Meta

    def get_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.user, context={'request': request}).data
    # end def

    def get_top_level_comments(self, obj):
        request = self.context.get("request")
        top_level_comments = ArticleComment.objects.filter(
            reply_to=None, article=obj)
        return ArticleCommentSerializer(top_level_comments, many=True, context={'request': request}).data
    # end def

    def get_engagements(self, obj):
        request = self.context.get("request")
        engagements = ArticleEngagement.objects.filter(article=obj)
        return ArticleEngagementSerializer(engagements, many=True, context={'request': request}).data
    # end def

    def get_current_user_liked(self, obj):
        request = self.context.get("request")
        print(request.user)
        if request.user.is_anonymous:
            return None
        else:
            user = request.user
            return ArticleEngagement.objects.filter(article=obj).filter(user=user).exists()
        # end if
    # end def
# end class


class ArticleEngagementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = ArticleEngagement
        fields = '__all__'
    # end Meta

    def get_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.user, context={'request': request}).data
    # end def
# end class


class CodeReviewSerializer(serializers.ModelSerializer):
    top_level_comments = serializers.SerializerMethodField(
        'get_top_level_comments')
    user = serializers.SerializerMethodField('get_user')
    likes = serializers.SerializerMethodField('get_likes')
    current_user_liked = serializers.SerializerMethodField('get_current_user_liked')

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

    def get_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.user, context={'request': request}).data
    # end def

    def get_likes(self, obj):
        return CodeReviewEngagement.objects.filter(code_review=obj).count()
    # end def

    def get_current_user_liked(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return None
        else:
            user = request.user
            return CodeReviewEngagement.objects.filter(code_review=obj).filter(user=user).exists()
        # end if-else
    # end def
# end class


class CodeReviewEngagementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = CodeReviewEngagement
        fields = '__all__'
    # end Meta

    def get_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.user, context={'request': request}).data
    # end def
# end class

