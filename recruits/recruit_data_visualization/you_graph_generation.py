import pandas as pd
from datetime import datetime
from wordcloud import WordCloud
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors
matplotlib.use('Agg')  # GUI 창을 띄우지 않도록 설정
from .you_data_processing import make_df
from django.conf import settings
import json
import os
# 운영 체제에 맞는 폰트 설정 (Mac, Windows, Linux)
import platform
current_os = platform.system()  # 다른 변수명 사용
if current_os == 'Windows': # 여기가 핵심 os 변수명에서 current_os 로 변경
    plt.rc('font', family='Malgun Gothic')
elif current_os == 'Darwin':
    plt.rc('font', family='AppleGothic')
elif current_os == 'Linux':
    plt.rc('font', family='NanumGothic')
else:
    print(f'{current_os} is not set')
def generate_wordcloud():
    df = make_df()
    # 제외하고 싶은 단어 리스트
    remove_words = ['기술 스택 없음', '기술스택', '외', '엔지니어링', '분석', '사이언' ,'인공지능','AI' ,'엔지니어']

    # 단어에 remove_words 리스트의 단어가 포함되어 있으면 제거
    def remove_unwanted_words(text_list):
        return ' '.join([word for word in text_list if not any(remove_word in word for remove_word in remove_words)])

    # stack이 리스트로 되어 있는 경우
    df_drop_category = df.groupby('category_name')['stack'].apply(
        lambda x: ' '.join([remove_unwanted_words(stack_list) for stack_list in x if isinstance(stack_list, list)])
    )

    font_path = os.path.join(settings.BASE_DIR, 'recruits/static/assets/NanumGothic.ttf')
    # 워드클라우드 생성 및 이미지로 변환
    wordcloud_images = {}
    for category, stack_words in df_drop_category.items():
        wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(stack_words)
        buffer = io.BytesIO()
        plt.figure(figsize=(7, 3))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graph = base64.b64encode(image_png).decode('utf-8')
        wordcloud_images[category] = graph
    return wordcloud_images

def generate_bar_graph(values):
    df = make_df()
    career_count = df['career'].value_counts()

    # 각 막대의 색상을 지정된 색상 코드로 설정
    hex_colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B']  # 바 그래프 색상 코드
    buffer = io.BytesIO()
    
    # 그래프 크기와 막대 너비 조정
    plt.figure(figsize=(3, 3.5))  # 너비와 높이 조정 (더 컴팩트하게)
    bars = plt.bar(career_count.index, career_count.values, color=hex_colors, width=0.6)  # 막대 너비 조정
    
    # 테마에 맞춰 그래프 스타일 설정 
    plt.xticks(fontsize=8, weight='bold', color='#333333')  # x축 라벨 크기와 굵기
    plt.yticks(fontsize=10, color='#333333')  # y축 라벨 크기
    plt.grid(False)  # y축 격자선 제거
    plt.tight_layout()  # 레이아웃 조정

    # 기존 막대 위에 데이터 개수 표시
    for bar, value in zip(bars, career_count.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value}',
                    ha='center', va='bottom', fontsize=10, weight='bold')
    
    # 그래프를 메모리 버퍼에 저장
    plt.savefig(buffer, format='png', transparent=True)  # 투명 배경
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # 이미지를 base64로 인코딩
    graph = base64.b64encode(image_png).decode('utf-8')
    
    return graph