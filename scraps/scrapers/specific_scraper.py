import datetime
from .base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class TheteamsScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.search_querys = ['데이터', '백엔드']

    def scrap(self):
        search_querys = self.search_querys
        # data_list = []
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:  
            for keword in search_querys:
                url = "https://www.theteams.kr/results/recruit/?search_query={}".format(keword)
                driver.get(url)

                while True:
                    # 현재 URL 출력
                    # print(f"Current URL: {driver.current_url}")
                    # 캡션 클래스 내부에 data를 수집
                    for element in driver.find_elements(By.CLASS_NAME, "caption"):
                        try:
                            category_element = element.find_element(By.CLASS_NAME, "badge_occupation") #카테고리 이름, ex)데이터 사이언스
                            # carrer_element = element.find_elements(By.TAG_NAME, "div")[1] #carrer, ex)신입/경력 , 비고 : 크롤링 페이지에서 요소 안보임.
                            title_element = element.find_element(By.TAG_NAME, "h4") #공고제목, ex) [숨고] Business Data Analyst
                            company_nm_element = element.find_element(By.TAG_NAME, "p") #회사이름, ex) (주)브레이브모바일
                            detial_url_element = element.find_element(By.TAG_NAME, "a") #디테일 페이지 주소
                            

                            job_info = {
                                        "title" : title_element.text.strip(),
                                        "company_name" : company_nm_element.text.strip(),
                                        "detail_url" : detial_url_element.get_attribute("href"),
                                        "end_date" : None,
                                        "platform_name" : "theteams",
                                        "category_name" : category_element.text.strip(),
                                        "stack" : None,
                                        "region" : None,
                                        "career" : None,
                            }
                            #요청 1개씩 바로바로 보내기
                            self.request_save(job_info)
                        except Exception as e:
                            print(f"Error extracting element data: {e}")
                    
                    # 수집한 후 next_page가 있으면 next_page로 이동
                    try:
                        page = driver.find_element(By.CLASS_NAME, "pagination")
                        li_elements = page.find_elements(By.TAG_NAME, "li")
                        
                        # 맨 마지막 엘리먼트는 '다음'이어야 함.
                        li_element = li_elements[-1]
                        if li_element.text.strip() == "다음":
                            print("Moving to the next page...")
                            a_element = li_element.find_element(By.TAG_NAME, "a")
                            a_element.click()  # 다음 페이지 클릭
                            # dom을 다시 reload 하기위해 페이지 새로고침
                            driver.refresh()
                            # time.sleep(1) 
                        else:
                            # 마지막 페이지일 경우 다음 keyword로 넘어감
                            break
                    except Exception as e:
                        print(f"Error navigating to next page: {e}")
                        break
        # self.request_save(data_list)


'''ex) surfit 플랫폼의 경우
1. 클래스의 첫번째 문자는 대문자 입니다.
2. 자신의 Scraper클래스를 만들고 BaseScraper 클래스를 상속받으세요.
3. 생성자 def __init__(self)를 구현하고 super().__init__()으로 부모생성자를 호출해주세요, 그 외에 필요한 필드를 직접 정의하세요.
4. BaseScraper 클래스의 def scrap(self) 는 추상메서드로 구현되어있습니다. 자식클래스에서 반드시 생성하신 후 그 안에다가 크롤링 코드를 넣어주세요.
5. BaseScraper 클래스에 데이터를 저장할 수 있는 def request_save(self, data) 가 구현되어있습니다. data는 1개씩 요청하세요.
6. driver를 이용하실 땐  
' with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver ' 를 이용해서 브라우저가 종료될 수 있도록 해주세요.
7. 코드를 다 작성하셨다면 scrapers > apps.py 파일에 들어가셔서 주석을 확인해주세요.
'''
class SurfitScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.search_querys = ['데이터', '백엔드']    
    
    #반드시 구현
    def scrap(self):
        
        #서버에 저장 요청하는 메서드
        data = {
            
        }
        self.request_save(data)
        pass

class SaraminScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.search_querys = ["데이터분석", "데이터 엔지니어", "데이터 사이언티스트"] 
        self.keyword_index = 0   
    
    def parse_end_date(self, date_text):
        if "오늘마감" in date_text:
            return datetime.datetime.now().strftime("%Y-%m-%d")
        if "내일마감" in date_text:
            return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if date_text.startswith("~ "):
            date_text = date_text[2:]
            try:
                current_year = datetime.datetime.now().year
                date_obj = datetime.datetime.strptime(f"{current_year}/{date_text[:5]}", "%Y/%m/%d")
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                pass
        return date_text
    
    def scrap(self):
        with webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="129.0.6668.89").install())) as driver:
            for page in range(200):
                current_keyword = self.search_querys[self.keyword_index]
                url = ('https://www.saramin.co.kr/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n'
                       f'&searchType=search&searchword={current_keyword}&recruitPage={page + 1}&recruitSort=relation&recruitPageCount=40')
                driver.get(url)

                job_elements = driver.find_elements(By.CLASS_NAME, "item_recruit")
                if not job_elements:
                    print("No more jobs found.")
                    break

                for job in job_elements:
                    try:
                        title_element = job.find_element(By.CSS_SELECTOR, "a").get_attribute("title")
                        title = title_element.strip() if title_element is not None else "No Title"
                        company_name = job.find_element(By.CSS_SELECTOR, "div.area_corp > strong > a").text.strip()
                        href = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        detail_url = "https://www.saramin.co.kr" + href if href is not None else "No URL"
                        org_end_date = job.find_element(By.CSS_SELECTOR, "div.job_date span.date").text
                        end_date = self.parse_end_date(org_end_date)
                        stack = [a.text.strip() for a in job.find_elements(By.CSS_SELECTOR, "div.job_sector > a")]
                        region = job.find_element(By.CSS_SELECTOR, "div.job_condition > span > a").text.strip()
                        career = job.find_element(By.CSS_SELECTOR, "div.job_condition > span:nth-child(2)").text.strip()

                        # Data dictionary to save
                        data = {
                            "title": title,
                            "company_name": company_name,
                            "detail_url": detail_url,
                            "end_date": end_date,
                            "platform_name": "saramin",
                            "category_name": current_keyword,
                            "stack": stack,
                            "region": region,
                            "career": career,
                        }
                        # Send data to the server
                        self.request_save(data)
                    except Exception as e:
                        print(f"Error extracting job data: {e}")

                self.keyword_index = (self.keyword_index + 1) % len(self.search_querys)