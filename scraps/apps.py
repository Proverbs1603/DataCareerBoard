from django.apps import AppConfig

class ScrapsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraps'

    #when django start, it starts too.
    def ready(self):
        from scraps.scrapers.specific_scraper import TheteamsScraper
        #스크래퍼 인스턴스 생성
        scraper = TheteamsScraper()
        # 60초마다 scrap 메서드 실행
        scraper.start_scraper_scheduler(interval_seconds=120)

        # 스케줄러 중지 예시 (필요할 때 중지)
        # scraper.stop_scraper_scheduler()
