# scraps/scrapers/apps.py
from django.apps import AppConfig

'''
1. 자기가 만든 Scraper 클래스를 import 하세요
2. 스크래퍼 인스턴스 생성
3. 아래 코드를 참고하셔서 인스턴스에서 start_scraper_scheduler를 호출하세요
4. 테스트 하실 땐 다른사람의 코드는 주석 처리하고 자신의 코드만 돌려서 확인해보세요.
5. 실행시킬 땐 'python.manage.py runserver --noreload' 로 실행시켜주세요
'''

class ScrapsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraps'

    #when django start, it starts too.
    def ready(self):
        from scraps.scrapers.specific_scraper import TheteamsScraper, RocketpunchScraper, SurfitScraper, SaraminScraper,JobplanetScraper, WantedScraper, ProgrammersScraper, CatchScraper, PeoplenJobScraper, IncruitScraper
        # 스크래퍼 인스턴스 생성
        theTeamScraper = TheteamsScraper()
        # 60초마다 scrap 메서드 실행 #test10초
        theTeamScraper.start_scraper_scheduler(interval_seconds=10)
        
        rocketpunchScraper = RocketpunchScraper()
        rocketpunchScraper.start_scraper_scheduler(interval_seconds=10)
        
        surfitScraper = SurfitScraper()
        surfitScraper.start_scraper_scheduler(interval_seconds=10)
        
        # saraminScraper = SaraminScraper()
        # saraminScraper.start_scraper_scheduler(interval_seconds=10)

        # jobplanetScraper = JobplanetScraper()
        # jobplanetScraper.start_scraper_scheduler(interval_seconds=10)

        # wantedScraper = WantedScraper()
        # wantedScraper.start_scraper_scheduler(interval_seconds=10)

        # #스크래퍼 인스턴스 생성
        # programmersScraper = ProgrammersScraper()
        # # 60초마다 scrap 메서드 실행 #test10초
        # programmersScraper.start_scraper_scheduler(interval_seconds=10)

        # catchscraper = CatchScraper()
        # catchscraper.start_scraper_scheduler(interval_seconds=10)

        # peoplenJobScraper = PeoplenJobScraper()
        # peoplenJobScraper.start_scraper_scheduler(interval_seconds=10)

        # incruitScraper = IncruitScraper()
        # incruitScraper.start_scraper_scheduler(interval_seconds=10)
