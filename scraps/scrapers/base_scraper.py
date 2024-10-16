from abc import abstractmethod
import requests
from apscheduler.schedulers.background import BackgroundScheduler

class BaseScraper():
    def __init__(self):
        self.base_url = "http://localhost:8000/api/recruit/"
        self.title = ""
        self.company_name = ""
        self.detail_url = ""
        self.end_date = ""
        self.platform_name = ""
        self.category_name = ""
        self.stack = ""
        self.region = ""  
        self.career = "" 
        self.scheduler = BackgroundScheduler()  # 스케줄러 초기화
    
    @abstractmethod
    def scrap(self):
        """
        스크래핑 작업을 수행하는 추상 메서드. 
        구체적인 스크래핑 로직은 자식 클래스에서 구현되어야 한다.
        """
        pass

    def request_save(self, data_list):
        try:
            for data in data_list:
                # POST 요청 보내기
                response = requests.post(self.base_url, json=data)
                response.raise_for_status()  # 응답 상태 확인 (예: 200 OK)
            
                # 요청이 성공했음을 출력 (응답 저장하지 않음)
                print(f"POST 요청 성공: {response.status_code}")
    
        except requests.exceptions.RequestException as e:
            print(f"POST 요청 실패: {e}")
    
    def start_scraper_scheduler(self, interval_seconds=60):
        """
        스케줄러를 시작하고 주기적으로 scrap 메서드를 실행
        """
        # 스크랩 메서드를 매 interval_seconds마다 실행하도록 스케줄 추가
        self.scheduler.add_job(self.scrap, 'interval', seconds=interval_seconds)
        self.scheduler.start()
        print(f"Scheduler started for class {self.__class__.__name__}, running every {interval_seconds} seconds.")

    def stop_scraper_scheduler(self):
        """
        스케줄러 중지
        """
        self.scheduler.shutdown()
        print("Scheduler stopped.")
            



