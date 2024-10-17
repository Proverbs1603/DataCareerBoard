import datetime
from .base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

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
class RocketpunchScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        
    def scrap(self):
        base_url = "https://www.rocketpunch.com"
        page_num = 1
        with webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="129.0.6668.101").install())) as driver:
            url = f"https://www.rocketpunch.com/jobs?page={page_num}&keywords=%EB%8D%B0%EC%9D%B4%ED%84%B0"
            driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            job_titles = soup.find_all('a', class_='nowrap job-title')
            if not job_titles:
                return
            
            for job in job_titles:
                
                # "데이터"와 무관한 공고가 검색이 많이 되서 필터링
                title = job.get_text().strip()
                if (not "데이터" in title) and (not "data" in title.lower()): 
                    continue
                
                job_info = {'title': title}
                
                job_url = base_url + job['href']
                driver.get(job_url)
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # 공고제목 - title, 회사이름 - company_name, 공고주소 - detail_url, 이미지주소 - img_link, 
                # 등록일 - pub_date, 마감일 - end_date, 카테고리 - category_name, 기술스택 - stack
                # 지역 - region, 신입/경력 - career
                job_info['company_name'] = soup.find_all('a', class_="nowrap company-name")[0].get_text().strip()
                job_info['detail_url'] = job_url
                
                end_date = soup.find('i', class_="ic-calendar_new icon").next_sibling.get_text().strip()
                job_info['end_date'] = end_date.split()[0]
                job_info['platform_name'] = "RocketPunch"
                
                job_info['category_name'] = None # 카테고리는 따로 없어서 추출하지 않음
                stacks = soup.select_one("#wrap > div.eight.wide.job-content.column > section:nth-child(5) > div").find_all('a')
                job_info['stack'] = [stack.get_text().strip() for stack in stacks]
                job_info['career'] = soup.select_one("body > div.pusher.dimmable > div.ui.vertical.center.aligned.detail.job-header.header.segment > div > div > div.job-stat-info").get_text().strip()

                # 지역의 경우 생략된 공고가 있어 예외처리
                region = soup.find(name='span', class_="address")
                if not region:
                    job_info['region'] = None
                else:
                    region = region.get_text().strip()
                    job_info['region'] = " ".join(region.split()[:2]) # 주소 텍스트에서 서울특별시 **구, 경기도 **시 까지만 저장
                
                self.request_save(job_info)
            page_num += 1


class SurfitScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.category_to_name = {
            "develop/data": "데이터 엔지니어",
            "develop/data-science": "데이터 사이언티스트",
            "develop/bigdata-ai-ml": "머신러닝 엔지니어",
            "planning/biz-analyst": "비즈니스 분석가"
        }
        self.cat_key = self.category_to_name.keys()
        
    #반드시 구현
    def scrap(self):
        sample = {'title':'sss', 'company_name':'test5', 'detail_url':'test', 'end_date':'2024-5-5', 'platform_name':'surfit','stack':[],'region':'경기도 양주시 고읍동', 'career':'무관'}
        self.request_save(sample)
        
        with webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="129.0.6668.101").install())) as driver:
            for cat in self.cat_key:
                base_url = f"https://jobs.surfit.io/{cat}" 

                driver.get(base_url)
                time.sleep(1)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤하는 동작이 없으면 공고가 로드되지 않음
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                job_titles = soup.find_all('span', class_="post-title")
                for job in job_titles:
                    job_info = {'title': job.get_text().strip()} # 공고 제목
                    job_url = job.find_parent('a')['href']
                    
                    driver.get(job_url)
                    time.sleep(3)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # 공고제목 - title, 회사이름 - company_name, 공고주소 - detail_url, 이미지주소 - img_link, 
                    # 등록일 - pub_date, 마감일 - end_date, 카테고리 - category_name, 기술스택 - stack
                    # 지역 - region, 신입/경력 - career
                    job_info['company_name'] = soup.select_one('#app > div.jobs > div > div > div > div > div.iTVFTT > div.zpulQ > div > div > span').get_text().strip()
                    job_info['detail_url'] = job_url
                    job_info['end_date'] = soup.select_one("#app > div.jobs > div > div > div > div > div.content-area.isNepE > div > div > ul > li:nth-child(3) > span.value").get_text().strip()
                    job_info['platform_name'] = "Surfit"
                    job_info['category_name'] = self.category_to_name[cat]
                    
                    stacks = soup.select_one("#app > div.jobs > div > div > div > div > div.content-area.isNepE > div > div > div.job-post-info > div:nth-child(2) > ul")
                    if not stacks:
                        job_info['stack'] = None
                    else:
                        stacks = stacks.find_all('li')
                        job_info['stack'] = [stack.get_text().strip() for stack in stacks]
                        
                    region = soup.find("span", class_="location-text").get_text().strip()
                    job_info['region'] = " ".join(region.split()[:2])  # 주소 텍스트에서 서울특별시 **구, 경기도 **시 까지만 저장
                    job_info['career'] = soup.select_one("#app > div.jobs > div > div > div > div > div.content-area.isNepE > div > div > ul > li:nth-child(1) > span.value").get_text().strip()
                    
                    self.request_save(job_info)

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