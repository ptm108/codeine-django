from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from .models import (
    CourseMaterial,
    CourseFile,
    Video,
    Quiz,
    Chapter,
    Course,
    Enrollment,
    Question,
    ShortAnswer,
    MCQ,
    MRQ,
    QuizResult,
    QuizAnswer,
    CourseReview,
    CourseComment,
    CourseCommentEngagement,
    QuestionGroup,
    QuestionBank
)

from common.models import Member, Partner
from common.serializers import NestedBaseUserSerializer, MemberSerializer

# Assessment related


class ShortAnswerSerializer(serializers.ModelSerializer):
    keywords = serializers.SerializerMethodField('get_keywords')

    class Meta:
        model = ShortAnswer
        fields = ('marks', 'keywords')
    # end class

    def get_keywords(self, obj):
        if self.context.get('public'):
            return None
        else:
            return obj.keywords
    # end def
# end class


class MCQSerializer(serializers.ModelSerializer):
    correct_answer = serializers.SerializerMethodField('get_correct_answer')

    class Meta:
        model = MCQ
        fields = ('marks', 'options', 'correct_answer')
    # end class
    # end class

    def get_correct_answer(self, obj):
        if self.context.get('public'):
            return None
        else:
            return obj.correct_answer
    # end def
# end class


class MRQAnswerSerializer(serializers.ModelSerializer):
    correct_answer = serializers.SerializerMethodField('get_correct_answer')

    class Meta:
        model = MRQ
        fields = ('marks', 'options', 'correct_answer')
    # end class

    def get_correct_answer(self, obj):
        if self.context.get('public'):
            return None
        else:
            return obj.correct_answer
    # end def
# end class


class QuestionSerializer(serializers.ModelSerializer):
    shortanswer = ShortAnswerSerializer()
    mcq = MCQSerializer()
    mrq = MRQAnswerSerializer()
    image = serializers.SerializerMethodField()
    question_bank = serializers.SerializerMethodField('get_label')

    class Meta:
        model = Question
        fields = ('id', 'title', 'subtitle', 'shortanswer', 'mcq', 'mrq', 'order', 'image', 'question_bank',)
    # end class

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        # end if
    # end def

    def get_label(self, obj):
        if obj.question_bank:
            return obj.question_bank.label
        else:
            return None
        # end if-else
    # end def
# end class


class QuestionBankSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuestionBank
        fields = '__all__'
    # end Meta
# end class


class CourseFileSerializer(serializers.ModelSerializer):
    zip_file = serializers.SerializerMethodField('get_zip_file_url')

    class Meta:
        model = CourseFile
        fields = ('zip_file', 'google_drive_url',)
    # end Meta

    def get_zip_file_url(self, obj):
        request = self.context.get("request")
        if obj.zip_file and hasattr(obj.zip_file, 'url'):
            return request.build_absolute_uri(obj.zip_file.url)
        # end if
    # end def
# end class


class CourseVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('video_url',)
    # end Meta
# end class


class QuestionGroupSerializer(serializers.ModelSerializer):
    question_bank = QuestionBankSerializer()

    class Meta:
        model = QuestionGroup
        fields = ('id', 'count', 'order', 'question_bank')
    # end Meta
# end class


class QuizSerializer(serializers.ModelSerializer):
    question_groups = QuestionGroupSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('id', 'passing_marks', 'course', 'course_material', 'instructions', 'is_randomized', 'question_groups',)
    # end Meta
# end class


class PublicCourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ('id', 'title', 'description', 'order', 'material_type',)
    # end Meta
# end class


class CourseMaterialSerializer(serializers.ModelSerializer):
    course_file = CourseFileSerializer()
    video = CourseVideoSerializer()
    quiz = QuizSerializer()

    class Meta:
        model = CourseMaterial
        fields = ('id', 'title', 'description', 'material_type', 'course_file', 'video', 'quiz', 'order')
    # end Meta
# end class


class ChapterSerializer(serializers.ModelSerializer):
    # course_materials = CourseMaterialSerializer(many=True)
    course_materials = serializers.SerializerMethodField('get_course_materials')

    class Meta:
        model = Chapter
        fields = ('id', 'title', 'overview', 'course_materials', 'order')
    # end Meta

    def get_course_materials(self, obj):
        request = self.context.get('request')
        owner = self.context.get('owner')
        pro_member = self.context.get('pro_member')

        # print('owner', owner)
        # print('pro_member', pro_member)
        # print(self.context.get('public'))

        if self.context.get('public'):
            # print(obj.course_materials)
            return PublicCourseMaterialSerializer(obj.course_materials, many=True).data
        elif not pro_member and not owner:  # pro course but member is under free tier
            return PublicCourseMaterialSerializer(obj.course_materials, many=True).data
        else:
            return CourseMaterialSerializer(obj.course_materials, many=True, context={'request': self.context.get('request')}).data
        # end if-else
    # end def

# end class


class CourseSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField('get_thumbnail_url')
    partner = serializers.SerializerMethodField('get_base_user')
    assessment = QuizSerializer()
    is_member_enrolled = serializers.SerializerMethodField('get_member_enrolled')

    class Meta:
        model = Course
        fields = '__all__'
    # end Meta

    def get_thumbnail_url(self, obj):
        request = self.context.get("request")
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            return request.build_absolute_uri(obj.thumbnail.url)
        # end if
    # end def

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.partner.user, context={'request': request}).data
    # end def

    def get_member_enrolled(self, obj):
        request = self.context.get("request")
        user = request.user

        if (type(user) == AnonymousUser):
            return None
        # end if

        member = Member.objects.filter(user=user).first()
        # print(obj)

        if member is None:
            return member
        else:
            enrollment = Enrollment.objects.filter(member=member).filter(course=obj)
            return enrollment.exists()
        # end if-else
    # end def

    def get_chapters(self, obj):
        request = self.context.get('request')
        user = request.user

        if not user.is_authenticated:
            return ChapterSerializer(obj.chapters, many=True, context=self.context).data
        # end if

        partner = Partner.objects.filter(user=user).first()
        member = Member.objects.filter(user=user).first()

        pro_member = member is not None and member.membership_tier == 'PRO' if obj.pro else True
        owner = obj.partner == partner

        context = {
            'public': self.context.get('public'),
            'request': request,
            'pro_member': pro_member,
            'owner': owner
        }

        return ChapterSerializer(obj.chapters, many=True, context=context).data
    # end def
# end class


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('progress', 'course', 'member', 'materials_done')
    # end Meta
# end class


class NestedEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ('progress', 'member', 'course', 'materials_done')
    # end Meta
# end class


class MemberEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    member = serializers.SerializerMethodField('get_base_user')

    class Meta:
        model = Enrollment
        fields = ('progress', 'member', 'course', 'materials_done')
    # end Meta

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
    # end def
# end class


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ('response', 'responses', 'quiz_result', 'question')
    # end Meta
# end class


class QuizResultSerializer(serializers.ModelSerializer):
    quiz_answers = QuizAnswerSerializer(many=True)

    class Meta:
        model = QuizResult
        fields = '__all__'
    # end Meta
# end class


class NestedQuizResultSerializer(serializers.ModelSerializer):
    quiz_answers = QuizAnswerSerializer(many=True)
    member = serializers.SerializerMethodField()

    class Meta:
        model = QuizResult
        fields = '__all__'
    # end Meta

    def get_member(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
    # end def
# end class


class CourseReviewSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('get_base_user')
    course_id = serializers.SerializerMethodField('get_course_id')

    class Meta:
        model = CourseReview
        fields = '__all__'
    # end Meta

    def get_base_user(self, obj):
        request = self.context.get("request")
        return NestedBaseUserSerializer(obj.member.user, context={'request': request}).data
    # end def

    def get_course_id(self, obj):
        return obj.course.id
    # end def
# end class


class ParentCourseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseComment
        fields = ('id', 'display_id')
    # end Meta
# end class


class NestedCourseCommentSerializer(serializers.ModelSerializer):
    user = NestedBaseUserSerializer()
    replies = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    current_member_liked = serializers.SerializerMethodField()
    reply_to = ParentCourseCommentSerializer()
    reply_count = serializers.SerializerMethodField('get_reply_count')

    class Meta:
        model = CourseComment
        fields = '__all__'
    # end Meta

    def get_replies(self, obj):
        request = self.context.get("request")
        if self.context.get("recursive"):
            return NestedCourseCommentSerializer(obj.replies, many=True, context={'request': request}).data
        else:
            return CourseCommentSerializer(obj.replies, many=True, context={'request': request}).data
        # end if else
    # end def

    def get_likes(self, obj):
        return CourseCommentEngagement.objects.filter(comment=obj).count()
    # end def

    def get_current_member_liked(self, obj):
        request = self.context.get("request")

        if hasattr(request.user, 'member'):
            member = request.user.member
            return CourseCommentEngagement.objects.filter(comment=obj).filter(member=member).exists()
        # end if
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

        return rec_reply_count(obj) - 1  # minus self
    # end def
# end class


class CourseCommentSerializer(serializers.ModelSerializer):
    user = NestedBaseUserSerializer()
    likes = serializers.SerializerMethodField()
    current_member_liked = serializers.SerializerMethodField()
    reply_to = ParentCourseCommentSerializer()
    reply_count = serializers.SerializerMethodField('get_reply_count')

    class Meta:
        model = CourseComment
        fields = '__all__'
    # end class

    def get_likes(self, obj):
        return CourseCommentEngagement.objects.filter(comment=obj).count()
    # end def

    def get_current_member_liked(self, obj):
        request = self.context.get("request")

        if hasattr(request.user, 'member'):
            member = request.user.member
            return CourseCommentEngagement.objects.filter(comment=obj).filter(member=member).exists()
        # end if
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

        return rec_reply_count(obj) - 1
    # end def
# end class
