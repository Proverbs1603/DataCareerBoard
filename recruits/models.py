from django.db import models

# **공고제목 - title**
# **회사명 - company_name**
# **디테일 페이지로 가는 주소 - detail_url **
# **마감일 - end_date**
# ** 참고한 플랫폼 이름 - platform_name**
class Recruit(models.Model):
    title = models.CharField(max_length=200, verbose_name='공고제목')
    company_name = models.CharField(max_length=200, verbose_name='회사명')
    detail_url = models.CharField(max_length=400, verbose_name='디테일 페이지 주소')
    end_date = models.CharField(max_length=11, default='수시채용', verbose_name='마감일') #수시채용 문자열 가능
    platform_name = models.CharField(max_length=50, verbose_name='가져온 플랫폼 이름' )
    
