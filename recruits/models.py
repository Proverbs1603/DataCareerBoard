from django.db import models

# **공고제목 - title**
# **회사명 - company_name**
# **디테일 페이지로 가는 주소 - detail_url **
# **마감일 - end_date**
# ** 참고한 플랫폼 이름 - platform_name**

# 새로 추가되는 필드들
# ** 카테고리 - category_name** -> 데이터 전처리 담당자가 결정권자
# ** 기술 스택 - stack **
# ** 지역  - region **
# ** 신입/경력 - career **

class Recruit(models.Model):
    title = models.CharField(max_length=200, verbose_name='공고제목')
    company_name = models.CharField(max_length=200, verbose_name='회사명')
    detail_url = models.CharField(max_length=400, verbose_name='디테일 페이지 주소')
    end_date = models.CharField(max_length=11, verbose_name='마감일', null=True, blank=True) #수시채용 문자열 가능
    platform_name = models.CharField(max_length=50, verbose_name='가져온 플랫폼 이름' )
    
    # 새로 추가되는 필드들
    # null=True: 데이터베이스 관점에서 필드가 NULL 값을 가질 수 있음을 의미
    # blank=True: Django 폼이나 관리자 페이지에서 필드를 비워둘 수 있음을 의미 (효과가 있을지는 마지막 완성본에서 검증 가능)
    category_name = models.CharField(max_length=100, verbose_name='카테고리', null=True, blank=True)  # 카테고리 정보 (예: 데이터 엔지니어, 머신러닝 등)
    stack = models.TextField(verbose_name='기술 스택', null=True, blank=True)  # 기술 스택 리스트 -> 문자열로 저장 (예: Python, AWS)
    region = models.CharField(max_length=200, verbose_name='지역', null=True, blank=True)  
    career = models.CharField(max_length=50, verbose_name='신입/경력', null=True, blank=True) 

    def __str__(self): # 직관적 출력 해당 메서드 정의 안할 시 <Recruit: Recruit object (1)> 
        return f'{self.title} - {self.company_name}'
    

# 변경사항 있을 시
# python manage.py makemigrations
# python manage.py migrate