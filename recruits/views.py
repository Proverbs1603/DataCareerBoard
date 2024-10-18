import os
from django.conf import settings
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from django.shortcuts import render
from .models import Recruit
from datetime import datetime, timedelta
from django.shortcuts import render
from .recruit_data_visualization.region_converter import convert_region
from .recruit_data_visualization.data_processing import get_job_data
from .recruit_data_visualization.graph_generation import create_line_and_pie_charts, create_choropleth
from .recruit_data_visualization.you_data_processing import make_df, get_closing_today_count, get_platform_count
from .recruit_data_visualization.you_graph_generation import generate_wordcloud, generate_bar_graph
from .recruit_data_visualization.all_count_visualiztion import get_data_count

def job_list(request):
    today = datetime.now()
    end_of_week = today + timedelta(days=7)
    recruits = Recruit.objects.filter(end_date__lte=end_of_week, end_date__gte=today)
    closing_today_count = get_closing_today_count()
    platform_count = get_platform_count()

     # 워드클라우드 이미지 생성 호출
    wordclouds = generate_wordcloud()

    # db_path와 table_name 정의
    db_path = 'db.sqlite3'  # SQLite3 데이터베이스 경로
    table_name = 'recruits_recruit'  # 테이블 이름

    # 데이터 개수 가져오기
    all_position_count = get_data_count(db_path, table_name)

    context = {
        'recruits' : recruits,
        'closing_today_count': closing_today_count,
        'platform_count': platform_count,
        'wordclouds': wordclouds,  # 추가된 부분
        'all_position_count' : all_position_count
        }
    
    return render(request, 'job_list.html', context)

    # recruits = Recruit.objects.all()

    # context = {'recruits' : recruits}
    # return render(request, 'job_list.html', context)

def job_table(request):
    recruits = Recruit.objects.all()
    context = {'recruits' : recruits}
    return render(request, 'job_table.html', context)

def job_graph(request):
    # 데이터 처리
    df, df_filtered = get_job_data()

    # 그래프 생성
    line_plot_html = create_line_and_pie_charts(df)
    choropleth_html = create_choropleth(df_filtered)
    wordclouds = generate_wordcloud()
    bar_graph = generate_bar_graph()

    # 컨텍스트 설정
    context = {
        'line_plot_html': line_plot_html,
        'choropleth_html': choropleth_html,
        'wordclouds': wordclouds,
        'bar_graph': bar_graph
    }

    # 템플릿 렌더링
    return render(request, 'job_graph.html', context)