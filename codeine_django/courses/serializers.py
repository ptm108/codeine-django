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
    CourseReview
)

from common.models import Member
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

    class Meta:
        model = Question
        fields = ('id', 'title', 'subtitle', 'shortanswer', 'mcq', 'mrq', 'order',)
    # end class
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


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('id', 'passing_marks', 'course', 'questions', 'instructions',)
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
        if (self.context.get('public')):
            # print(obj.course_materials)
            return PublicCourseMaterialSerializer(obj.course_materials, many=True).data
        else:
            return CourseMaterialSerializer(obj.course_materials, many=True, context={'request': self.context.get('request')}).data
        # end if-else
    # end def

# end class


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True)
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
        print(obj)

        if member is None:
            return member
        else:
            enrollment = Enrollment.objects.filter(member=member).filter(course=obj)
            return enrollment.exists()
        # end if-else
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
        fields = ('progress', 'member', 'course', 'chapters_done')
    # end Meta
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


class CourseReviewSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('get_base_user')
    course_id = serializers.SerializerMethodField('get_course_id')

    class Meta:
        model = CourseReview
        fields = '__all__'
    # end Meta

    def get_base_user(self, obj):
        return NestedBaseUserSerializer(obj.member.user).data
    # end def

    def get_course_id(self, obj):
        return obj.course.id
    # end def
# end class
