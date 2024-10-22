import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import json
from django.conf import settings
from plotly.subplots import make_subplots
from shapely.geometry import shape

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

# GeoJSON 파일에서 각 지역의 중심 좌표와 폴리곤 면적을 계산하는 함수
def get_center_and_area(geojson_data):
    centers = {}
    for feature in geojson_data['features']:
        region_name = feature['properties']['CTP_KOR_NM']
        polygon = shape(feature['geometry'])
        
        # 폴리곤의 중심과 면적 계산
        centroid = polygon.centroid
        area = polygon.area
        
        centers[region_name] = {
            'lon': centroid.x,
            'lat': centroid.y,
            'area': area
        }
    return centers

def create_choropleth(df_filtered):
    # GeoJSON 파일 경로
    geojson_path = os.path.join(settings.BASE_DIR, 'recruits', 'static', 'assets', 'TL_SCCO_CTPRVN.json')
    with open(geojson_path, encoding='utf-8') as f:
        geojson_data = json.load(f)

    # 모든 지역에 대한 기본 카운트를 0으로 설정
    all_regions = [feature['properties']['CTP_KOR_NM'] for feature in geojson_data['features']]
    default_counts = pd.DataFrame({
        'Region': all_regions,
        'Counts_default': [0] * len(all_regions)  # 모든 지역에 기본 값 0 할당
    })

    # 실제 데이터에서 지역별 카운트를 가져옴
    region_counts = df_filtered['region_converted'].value_counts()
    region_jobs_df = pd.DataFrame({
        'Region': region_counts.index,
        'Counts_actual': region_counts.values
    })

    # 기본 카운트 데이터와 실제 데이터 병합 (실제 데이터가 있으면 덮어씀)
    merged_df = pd.merge(default_counts, region_jobs_df, on='Region', how='left')

    # 결측치를 처리하여 실제 값이 있으면 그 값을 사용하고, 없으면 기본값 0을 사용
    merged_df['Counts'] = merged_df['Counts_actual'].fillna(merged_df['Counts_default'])

    # Choropleth 만들기 (매핑되지 않은 지역의 색상을 '#F9F9F9'로 지정)
    fig_choropleth = px.choropleth(merged_df,
                                   geojson=geojson_data,
                                   locations='Region',
                                   featureidkey='properties.CTP_KOR_NM',
                                   color='Counts',
                                   color_continuous_scale='Blues',
                                   range_color=[1, merged_df['Counts'].max()],
                                   width=600, height=700)

    # 마우스를 올렸을 때 Counts 값이 표시되도록 hovertemplate 설정
    fig_choropleth.update_traces(
        hovertemplate='<b>%{location}</b><br>Counts: %{z}<extra></extra>',
        marker_line_color='black'  # 지도 경계선 색을 명확히 설정
    )

    # 지도의 세부 설정 (육지와 바다의 색상 조정)
    fig_choropleth.update_geos(
        visible=False,
        projection_scale=25,  # 축소하여 지도가 위아래로 잘리지 않도록 조정
        center={"lat": 35.8, "lon": 127.8},  # 지도의 중심을 약간 위로 조정
        showland=True,
        landcolor="white",  # 매핑되지 않은 지역의 색상
        showframe=False,
        showcoastlines=False,
        lonaxis_range=[140, 230]  # 동서 방향의 범위 제한 (경도 범위 설정)
    )

    # 레이아웃 수정 (범례 제거, 여백 조정)
    fig_choropleth.update_layout(
        dragmode=False,
        geo=dict(showframe=False, showcoastlines=False, showland=True, landcolor="white"),
        coloraxis_showscale=False,  # 컬러바(범례) 제거
        autosize=False,  # autosize 비활성화
        margin={"r": 0, "t": 0, "l": 0, "b": 0},  # 위, 아래 여백을 없앰
    )

    # 각 지역의 중심 좌표와 면적을 계산
    region_centers = get_center_and_area(geojson_data)

    # 글자 크기 설정
    font_size = 9

    # Scattergeo로 각 지역의 중심 좌표에 텍스트를 표시
    lon_values = [region_centers[region]['lon'] for region in merged_df['Region']]
    lat_values = [region_centers[region]['lat'] for region in merged_df['Region']]

    # 경기도(경기) 지역만 별도로 위치 조정
    if '경기도' in merged_df['Region'].values:
        idx = merged_df['Region'].tolist().index('경기도')
        lon_values[idx] += 0.2  # 경기도의 글자를 오른쪽으로 이동

    fig_choropleth.add_trace(go.Scattergeo(
        lon=lon_values,
        lat=lat_values,
        text=merged_df['Counts'],  # 각 지역의 Counts 값 표시
        mode='text',  # 텍스트만 표시
        textfont=dict(size=font_size, color="#8BD8BD", family="Arial Black"),  # 폰트 크기와 스타일 설정
        textposition="middle center",  # 텍스트 위치를 중앙으로 설정
        showlegend=False,  # 범례 숨기기
        hoverinfo="skip"  # hover 정보 생략
    ))

    ### 막대 및 선 그래프 변경 시작 ###

    # 상위 3개 지역을 선택하고 나머지를 "그 외 지역"으로 묶기
    top_3_df = merged_df.nlargest(3, 'Counts')  # 상위 3개 지역
    others_count = merged_df['Counts'].sum() - top_3_df['Counts'].sum()  # 나머지 지역 합계

    # "그 외 지역" 추가
    others_df = pd.DataFrame({
        'Region': ['그 외 지역'],
        'Counts': [others_count]
    })

    # 상위 3개 + "그 외 지역" 결합
    final_df = pd.concat([top_3_df, others_df])

    # 막대 그래프 생성 (파란색 계열)
    bar_trace = go.Bar(
        x=final_df['Region'],
        y=final_df['Counts'],
        name='Counts',
        marker_color='#A1C2F1',  # 중간 정도의 파란색
        marker_line=dict(width=1.5, color='#5A96E3'),  # 진한 파란색 외곽선
        opacity=0.85,  # 막대 투명도 설정
        width=0.6,  # 막대 너비 조정
        showlegend=False  # 범례 숨김
    )

    # 선 그래프 생성 (밝은 파란색 계열)
    line_trace = go.Scatter(
        x=final_df['Region'],
        y=final_df['Counts'],
        name='Counts Line',
        mode='lines+markers',
        marker=dict(color='#4A90E2', size=8),  # 마커 크기와 색상 설정
        line=dict(width=2, dash='solid'),  # 선 스타일과 두께 조정
        showlegend=False  # 범례 숨김
    )

    # 막대 및 선 그래프를 결합하여 새로운 그래프 생성
    fig_graph = go.Figure()
    fig_graph.add_trace(bar_trace)
    fig_graph.add_trace(line_trace)

    # 막대-선 그래프 레이아웃 설정 (위로 올림 + 배경색 설정)
    fig_graph.update_layout(
        height=200,  # 그래프 높이를 줄여서 지도 바로 밑에 표시되도록 설정
        margin={"r": 0, "t": 10, "l": 0, "b": 0},  # 그래프 내부 여백 최소화
        yaxis=dict(showgrid=False, zeroline=False, linecolor='white', showticklabels=False),  # Y축 숫자 라벨 제거
        xaxis=dict(showgrid=False, zeroline=False, linecolor='white'),  # X축 설정
        plot_bgcolor='white',  # 그래프 내부 배경색
    )

    # Choropleth 지도 HTML과 추가 그래프 HTML 결합하여 반환
    choropleth_html = fig_choropleth.to_html(full_html=False)
    graph_html = fig_graph.to_html(full_html=False)

    # 두 그래프를 하나의 박스 안에 배치하는 스타일 설정
    combined_html = f"""
    <div style="margin: 0; padding: 0;">
        {choropleth_html}
    </div>
    <div style="margin: 0; padding: 0; position: relative; top: -20px;">  <!-- 그래프 위치를 조금만 위로 올림 -->
        {graph_html}
    </div>
    """

    return combined_html
