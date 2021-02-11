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
)

# Assessment related


class ShortAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortAnswer
        fields = ('question', 'marks', 'keywords')
    # end class
# end class


class MCQSerializer(serializers.ModelSerializer):

    class Meta:
        model = MCQ
        fields = ('question', 'marks', 'options', 'correct_answer')
    # end class
# end class


class MRQAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MRQ
        fields = ('question', 'marks', 'options', 'correct_answer')
    # end class
# end class


class QuestionSerializer(serializers.ModelSerializer):
    shortanswer = ShortAnswerSerializer()
    mcq = MCQSerializer()
    mrq = MRQAnswerSerializer()

    class Meta:
        model = Question
        fields = ('title', 'subtitle', 'shortanswer', 'mcq', 'mrq',)
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
        fields = ('id', 'passing_marks', 'course', 'questions',)
    # end Meta
# end class


class PublicCourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ('id', 'title', 'description', 'order',)
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
            print(obj.course_materials)
            return PublicCourseMaterialSerializer(obj.course_materials, many=True).data
        else:
            return CourseMaterialSerializer(obj.course_materials, many=True, context={'request': self.context.get('request')}).data
        # end if-else
    # end def

# end class


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True)
    thumbnail = serializers.SerializerMethodField('get_thumbnail_url')

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
# end class


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
    # end Meta
# end class
