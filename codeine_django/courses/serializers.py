from rest_framework import serializers

from .models import (Section, Chapter, Course)


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
        if obj.profile_photo and hasattr(obj.profile_photo, 'url'):
            return request.build_absolute_uri(obj.profile_photo.url)
        # end if
    # end def
# end class

