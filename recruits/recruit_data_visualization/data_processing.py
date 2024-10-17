import pandas as pd
from recruits.models import Recruit
from .region_converter import convert_region  # 지역 변환 함수는 별도로 모듈화

def get_job_data():
    # Recruit 데이터베이스에서 모든 데이터를 가져옴
    recruits = Recruit.objects.all().values()
    df = pd.DataFrame(recruits)

    # 데이터 처리: 'platform_name'과 'category_name'이 없을 경우 기본값 지정
    df['platform_name'] = df.get('platform_name', 'Unknown')
    df['category_name'] = df.get('category_name', 'Unknown')

    # 지역 변환 및 시/도별 채용 공고 수 데이터 생성
    df['region_converted'] = df['region'].apply(convert_region)
    df_filtered = df.dropna(subset=['region_converted'])

    return df, df_filtered
