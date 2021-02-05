from rest_framework import serializers

from .models import (
    Section,
    Chapter,
    Course,
    Enrollment,
    Question,
    ShortAnswer,
    MCQ,
    MRQ,
    Assessment
)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'title', 'description', 'video_url', 'google_drive_link')
    # end Meta
# end class


class ChapterSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ('id', 'title', 'overview', 'sections')
        # end Meta
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
        fields = ('title', 'subtitle',)
    # end class
# end class


class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Assessment
        fields = ('id', 'passing_grade', 'course', 'questions')
    # end Meta
# end class
