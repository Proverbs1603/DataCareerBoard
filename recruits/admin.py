from django.contrib import admin
from .models import Recruit

# Register your models here.
# class RecruitAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('title', {'fields': ['title'], 'description': ['공고제목']}),    
#     ]
#     #readonly_fields = ['end_date'] #읽기모드
#     list_display = ('title', 'company_name', 'end_date') #admin 목록 페이지에 나오는 것들.
#     list_filter = ['end_date'] #필터옵션제공 
#     search_fields = ['title', 'company_name'] #question_text 또는 choice_text에 따라 검색 가능

admin.site.register(Recruit)