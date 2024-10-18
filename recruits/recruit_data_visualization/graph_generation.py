import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import json
from django.conf import settings
from .data_processing import get_job_data

def create_line_and_pie_charts(df):
    platform_counts = df['platform_name'].value_counts()
    platform_jobs_df = pd.DataFrame({
        'Platform': platform_counts.index,
        'Counts': platform_counts.values
    })

    category_counts = df['category_name'].value_counts()
    category_jobs_df = pd.DataFrame({
        'Category': category_counts.index,
        'Counts': category_counts.values
    })

    # 카테고리의 요소 수에 따라 색상 배열을 동적으로 생성
    base_color = 'rgba(135, 162, 255, {opacity})'  # 기본 색상
    total_counts = category_jobs_df['Counts'].sum()  # 전체 카테고리 값의 합
    num_categories = len(category_jobs_df['Category'])
    
    # 각 카테고리의 비율에 따라 투명도를 적용한 색상 생성
    colors = []
    for i, count in enumerate(category_jobs_df['Counts']):
        ratio = count / total_counts  # 각 카테고리의 비율 계산
        opacity = 1 - (0.8 * i / (num_categories - 1))  # 투명도를 0.2 ~ 1.0 범위에서 계산
        rgba_color = base_color.format(opacity=opacity)  # 투명도를 적용한 색상
        colors.append(rgba_color)

    fig = go.Figure()

    # 라인플롯 추가
    fig.add_trace(go.Scatter(x=platform_jobs_df['Platform'],
                             y=platform_jobs_df['Counts'],
                             mode='lines+markers',
                             name='플랫폼 별 채용 공고',
                             visible=True))

    # 파이차트 추가
    fig.add_trace(go.Pie(labels=category_jobs_df['Category'],
                         values=category_jobs_df['Counts'],
                         marker=dict(colors=colors),
                         textinfo='percent',
                         textposition='inside',
                         hoverinfo='label+percent',
                         name='카테고리 별 채용 공고',
                         visible=False,
                         showlegend=True)) 

    fig.update_layout(
        updatemenus=[dict(type="buttons", direction="right", x=0.5, y=1.2, xanchor='center', yanchor='top',
                          buttons=[dict(label="플랫폼 별 채용 공고", method="update", args=[{"visible": [True, False]},
                                                                                      {"yaxis": {"visible": True},
                                                                                       "plot_bgcolor": "rgba(135, 162, 255, 0.2)"}]),
                                   dict(label="카테고리 별 채용 공고", method="update", args=[{"visible": [False, True]},
                                                                                      {"yaxis": {"visible": False},
                                                                                       "plot_bgcolor": "rgba(255, 255, 255, 1)"}])])],
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        plot_bgcolor="rgba(135, 162, 255, 0.2)",  # 라인플롯의 배경색 유지
        paper_bgcolor="rgba(255, 255, 255, 1)",
        width=600, height=400,
    )

    # 파이차트로 변경 시 y축 제거 및 배경색 변경
    fig.update_layout(
        yaxis=dict(visible=True if fig.data[0].visible else False),  # 라인플롯일 때 y축 유지, 파이차트일 때 제거
    )

    return fig.to_html(full_html=False)



def create_choropleth(df_filtered):
    # GeoJSON 파일 경로
    geojson_path = os.path.join(settings.BASE_DIR, 'recruits', 'static', 'assets', 'TL_SCCO_CTPRVN.json')
    with open(geojson_path, encoding='utf-8') as f:
        geojson_data = json.load(f)

    # 모든 지역에 대한 기본 카운트를 1로 설정
    all_regions = [feature['properties']['CTP_KOR_NM'] for feature in geojson_data['features']]
    default_counts = pd.DataFrame({
        'Region': all_regions,
        'Counts': [1] * len(all_regions)  # 모든 지역에 기본 값 1 할당
    })

    # 실제 데이터에서 지역별 카운트를 가져옴
    region_counts = df_filtered['region_converted'].value_counts()
    region_jobs_df = pd.DataFrame({
        'Region': region_counts.index,
        'Counts': region_counts.values
    })

    # 기본 카운트 데이터와 실제 데이터 병합 (실제 데이터가 있으면 덮어씀)
    merged_df = pd.merge(default_counts, region_jobs_df, on='Region', how='left', suffixes=('_default', '_actual'))
    merged_df['Counts'] = merged_df['Counts_actual'].fillna(merged_df['Counts_default'])
    
    fig_choropleth = px.choropleth(merged_df,
                                   geojson=geojson_data,
                                   locations='Region',
                                   featureidkey='properties.CTP_KOR_NM',
                                   color='Counts',
                                   title='시/도별 채용 공고 수',
                                   color_continuous_scale='Blues',
                                   width=900, height=700,
                                   range_color=[1, merged_df['Counts'].max()])


    fig_choropleth.update_geos(
        fitbounds="locations",
        visible=False,
        projection_scale=7,
        center={"lat": 36.5, "lon": 127.5},
        showland=True,
        landcolor="white",
        showframe=False,
        showcoastlines=False
    )

    fig_choropleth.update_layout(
        dragmode=False,
        geo=dict(showframe=False, showcoastlines=False, showland=True, landcolor="white")
    )

    return fig_choropleth.to_html(full_html=False)
