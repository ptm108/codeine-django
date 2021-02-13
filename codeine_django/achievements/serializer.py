from rest_framework import serializers
from .models import (
    Achievement, 
    AchievementRequirement
)

class AchievementRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementRequirement
        fields = '__all__'
    # end Meta
# end class

class AchievementSerializer(serializers.ModelSerializer):
    achievement_requirements = AchievementRequirementSerializer(many=True)
    badge = serializers.SerializerMethodField('get_badge_url')

    class Meta:
        model = Achievement
        fields = '__all__'
    # end Meta

    def get_badge_url(self, obj):
        request = self.context.get("request")
        if obj.badge and hasattr(obj.badge, 'url'):
            return request.build_absolute_uri(obj.badge.url)
        # end if
    # end def
# end class