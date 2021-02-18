from rest_framework import serializers
from .models import (
    IndustryProject, 
    IndustryProjectApplication
)

class IndustryProjectApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryProjectApplication
        fields = '__all__'
    # end Meta
# end class

class IndustryProjectSerializer(serializers.ModelSerializer):
    industry_project_applications = IndustryProjectApplicationSerializer(many=True)

    class Meta:
        model = IndustryProject
        fields = '__all__'
    # end Meta
# end class