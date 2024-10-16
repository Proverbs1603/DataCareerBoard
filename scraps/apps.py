from django.apps import AppConfig

class ScrapsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraps'

    #when django start, it starts too.
    def ready(self):
        from scraps.scrapers.specific_scraper import TheteamsScraper
        #스크래퍼 인스턴스 생성
        theTeamScraper = TheteamsScraper()
        # 60초마다 scrap 메서드 실행 #test10초
        theTeamScraper.start_scraper_scheduler(interval_seconds=10)
