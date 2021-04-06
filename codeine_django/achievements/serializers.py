from rest_framework import serializers
from .models import (
    Achievement,
    AchievementRequirement,
    MemberAchievement
)


class AchievementRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementRequirement
        fields = '__all__'
    # end Meta
# end class


class FullAchievementRequirementSerializer(serializers.ModelSerializer):
    stat = serializers.SerializerMethodField('get_full_stat')

    class Meta:
        model = AchievementRequirement
        fields = '__all__'
    # end Meta

    def get_full_stat(self, obj):
        if obj.stat == "PY":
            return "Python"
        if obj.stat == "JAVA":
            return "Java"
        if obj.stat == "JS":
            return "Javascript"
        if obj.stat == "CPP":
            return "C++"
        if obj.stat == "CS":
            return "C#"
        if obj.stat == "RUBY":
            return "Ruby"
        if obj.stat == "SEC":
            return "Security"
        if obj.stat == "DB":
            return "Database Administration"
        if obj.stat == "FE":
            return "Frontend"
        if obj.stat == "BE":
            return "Backend"
        if obj.stat == "UI":
            return "UI/UX"
        if obj.stat == "ML":
            return "Machine Learning"
        # end ifs
        return obj.stat
    # end def
# end class


class FullAchievementSerializer(serializers.ModelSerializer):
    achievement_requirements = FullAchievementRequirementSerializer(many=True)
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


class MemberAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()

    class Meta:
        model = MemberAchievement
        fields = ('achievement',)
    # end Meta
# end class
