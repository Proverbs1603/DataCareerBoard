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
os = platform.system()

if os == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif os == 'Darwin':
    plt.rc('font', family='AppleGothic')
elif os == 'Linux':
    plt.rc('font', family='NanumGothic')
else:
    print(f'{os} is not set')


def generate_wordcloud():
    df = make_df()
    category_stack = df.groupby('category_name')['stack'].apply(lambda x: ' '.join([str(i) if i is not None else '' for i in x]))
    
    font_path = "/Users/youyoungcheon/Desktop/visual/django-myapp/recruits/static/assets/NanumGothic.ttf"
    # 워드클라우드 생성 및 이미지로 변환
    wordcloud_images = {}
    for category, stack_words in category_stack.items():
        wordcloud = WordCloud(width=800, height=400, background_color='white', font_path = font_path).generate(stack_words)
        buffer = io.BytesIO()
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graph = base64.b64encode(image_png).decode('utf-8')
        wordcloud_images[category] = graph

    return wordcloud_images

# 신입/경력 공고 수 비율 그래프 생성
def generate_bar_graph():
    df = make_df()
    career_count = df['career'].value_counts()

    # 각 막대의 색상을 다르게 설정: 서로 다른 투명도를 포함한 rgba 값
    rgba_colors = [
        (135/255, 162/255, 255/255, 1.0),  # 첫 번째 막대
        (135/255, 162/255, 255/255, 0.5),  # 두 번째 막대
        (135/255, 162/255, 255/255, 0.2),  # 세 번째 막대
        (135/255, 162/255, 255/255, 0.1)   # 네 번째 막대
    ]
    hex_colors = [mcolors.to_hex(c) for c in rgba_colors]

    buffer = io.BytesIO()
    plt.figure(figsize=(8, 4))
    career_count.plot(kind='bar', color=hex_colors)
    plt.title('신입/경력 공고 수 비율')
    plt.tight_layout()

    plt.savefig(buffer, format='png')  # 그래프를 메모리 버퍼에 저장
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode('utf-8')

    return graph