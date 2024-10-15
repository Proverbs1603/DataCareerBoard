from recruits.models import Recruit
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class RecruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruit
        fields = ['title', 'company_name', 'detail_url', 'end_date', 'platform_name']

        validators = [
            UniqueTogetherValidator(
                queryset=Recruit.objects.all(),
                fields=['title', 'company_name']
            )
        ]        