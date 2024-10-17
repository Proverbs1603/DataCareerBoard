import pandas as pd
from recruits.models import Recruit

import pandas as pd
from datetime import datetime

def make_df():
    # Django ORM을 사용해 데이터베이스에서 데이터 조회
    recruits = Recruit.objects.all().values()

    # Pandas 데이터프레임으로 변환
    df = pd.DataFrame(list(recruits))
    
    return df

def get_closing_today_count():
    df = make_df()
    today = datetime.now().strftime('%Y-%m-%d')
    closing_today_count = len(df[df['end_date'] == today])
    return closing_today_count

def get_platform_count():
    df = make_df()
    platform_count = df['platform_name'].nunique()
    return platform_count
