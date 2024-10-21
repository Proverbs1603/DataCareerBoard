import pandas as pd
from recruits.models import Recruit

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

#지역
def convert_region(region):
    regions_dict = {
    '서울': '서울특별시',
    '부산': '부산광역시',
    '대구': '대구광역시',
    '인천': '인천광역시',
    '광주': '광주광역시',
    '대전': '대전광역시',
    '울산': '울산광역시',
    '세종': '세종특별자치시',
    '경기': '경기도',
    '강원': '강원도',
    '충북': '충청북도',
    '충남': '충청남도',
    '전북': '전라북도',
    '전남': '전라남도',
    '경북': '경상북도',
    '경남': '경상남도',
    '제주': '제주특별자치도'
}
    
    if region is None:
        return None
    for key in regions_dict:
        if region.startswith(key):
            return regions_dict[key]
    return None