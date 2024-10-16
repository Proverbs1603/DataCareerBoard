from recruits.models import Recruit
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class RecruitSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        #태현님 이곳에서 전처리 작업하시면 됩니다.
        return attrs


    class Meta:
        model = Recruit
        fields = ['title', 'company_name', 'detail_url', 'end_date', 'platform_name']

        validators = [
            UniqueTogetherValidator(
                queryset=Recruit.objects.all(),
                fields=['title', 'company_name'],
                message="이 회사에서는 이미 같은 제목의 공고가 존재합니다.",  # 커스터마이즈된 메시지
            )
        ]        