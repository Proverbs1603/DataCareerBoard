from recruits.models import Recruit
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from datetime import datetime

class RecruitSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        #태현님 이곳에서 전처리 작업하시면 됩니다.
        
        attrs['category_name'] = self.category_name(attrs['title'])
        keys = ['end_date', 'career','region','stack']
        
        print(attrs.keys())
        for key in keys:
            if key in attrs.keys():
                attrs[key] = getattr(self, key, None)(attrs[key])
            else:
                print(f"Missing {key} attribute.")
                attrs[key] = None
        
        print(f"Validated data: {attrs}")
        return attrs
    
    
    class Meta:
        model = Recruit
        fields = '__all__'
        read_only_fields = ['pub_date']  # 생성일은 읽기 전용으로 설정
        # fields = ['title', 'company_name', 'detail_url', 'end_date', 'platform_name']

        validators = [
            UniqueTogetherValidator(
                queryset=Recruit.objects.all(),
                fields=['title', 'company_name'],
                message="이 회사에서는 이미 같은 제목의 공고가 존재합니다.",  # 커스터마이즈된 메시지
            )
        ]        
    
    
    def category_name(self, title):
        ds = ["과학", "scientist", "science", "research", "사이언", "r&d", "연구", "ml", "ai", "머신", "machine", "인공지능", "deep", "computer vision", "컴퓨터 비전", 'llm']
        da = ["분석", "analy", "애널리"]
        de = ["데이터 엔지니어", "데이터엔지니어", "engineer, data", "engineer(data)", "engineer (Data)", "데이터 개발자", "data engineer", "warehouse", "dw", "bi", "etl", "pipeline", "infra", "플랫폼", "platform"]
    
        for keyword in ds:
            if keyword in title.lower():
                return "데이터 사이언티스트"
            
        for keyword in da:
            if keyword in title.lower():
                return "데이터 분석가"
            
        for keyword in de:
            if keyword in title.lower():
                return "데이터 엔지니어"
        
        return "미분류" # 데이터 관련 직무로 볼 수 없음
    
    def end_date(self, date):
        words = ['채용', '수시', '상시']
        #yy.mm.dd, 수시채용, yyyy-mm-dd, yyyy.mm.dd, 채용시, 상시채용, N/A, 채용시까지, 상시, mm/dd
        if not date or date == "N/A":
            return None

        for word in words:
            if word in date:
                return "상시채용"
            
        #print(date)
        if date.count("-") == 2:
            return date
        elif date.count(".") == 2:
            year, month, day = date.split(".")
        elif date.count("/") == 1: #mm/dd
            month, day = date.split("/")
            if int(month) < datetime.now().month:
                year = str(int(year) + 1)
            else:
                year = datetime.now().year
                    
        return f"{year}-{month}-{day}"
    
    def career(self, career):
        junior_senior = ['신입·경력', '무관', '0']
        if career == 'N/A':
            return None

        if "경력(연차무관)" == career:
            return "경력"
        
        for i in junior_senior:
            if i in career:
                return "신입·경력"
        
        if "경력" in career or "년" in career:
            return "경력"
        
        if "신입" in career:
            return "신입"
        
        if "인턴" in career:
            return "인턴"
        
        return None
    
    def region(self, region):
        if region == 'N/A' or region == '지역' or not region:
            return None
        
        if region == "재택근무" or region == "100% 원격근무":
            return "재택근무"
        
        region_len = len(region.split())
        if region_len == 1:
            return region
        elif region_len >= 2:
            return ' '.join(region.split()[:2])
    
    def stack(self, stack):
        if stack == 'N/A' or not stack:
            return ["기술 스택 없음"]
        else:
            return stack