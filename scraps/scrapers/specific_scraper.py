import datetime
from .base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from datetime import datetime, timedelta

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

class RocketpunchScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        
    def scrap(self):
        base_url = "https://www.rocketpunch.com"
        page_num = 1
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
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
        
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
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
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
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
                        detail_url = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
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

class WantedScraper(BaseScraper): # jk
    def __init__(self):
        super().__init__()

    def scrape_additional_info(self, url):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        try:
            driver.get(url)
            time.sleep(3)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            career_element = soup.find("span", string=lambda text: text is not None and ("경력" in text or "신입" in text))
            career = career_element.get_text(strip=True) if career_element else "경력 정보 없음"

            stack_heading = soup.find("h2", text="기술 스택 • 툴")
            stack_elements = stack_heading.find_next("ul").find_all("span", class_="Typography_Typography__root__RdAI1 Typography_Typography__label2__svmAA Typography_Typography__weightMedium__GXnOM") if stack_heading else None
            stack = [el.get_text(strip=True) for el in stack_elements] if stack_elements else ["기술 스택 없음"]

            end_date_element = soup.find("span", class_="Typography_Typography__root__RdAI1 Typography_Typography__body1-reading__3pEGb Typography_Typography__weightRegular__jzmck")
            end_date = end_date_element.get_text(strip=True) if end_date_element else "마감일 정보 없음"

            region_element = soup.find("span", class_="Typography_Typography__root__RdAI1 Typography_Typography__body2__5Mmhi Typography_Typography__weightMedium__GXnOM")
            region = region_element.get_text(strip=True) if region_element else "근무 지역 정보 없음"

            return {
                "end_date": end_date,
                "career": career,
                "region": region,
                "stack": stack
            }

        except Exception as e:
            print(f"Error while scraping {url}: {e}")
            return {
                "end_date": "마감일 정보 없음",
                "career": "경력 정보 없음",
                "region": "근무 지역 정보 없음",
                "stack": ["기술 스택 없음"]
            }
        finally:
            driver.quit()

    def scrap(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0&tab=position")
        driver.implicitly_wait(5)
        time.sleep(5)

        scroll_pause_time = 1
        scroll_limit = 1

        for _ in range(scroll_limit):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        job_cards = soup.find_all("div", class_="JobCard_container__REty8")
        jobs_data = []

        def process_job(job_card):
            base_url = "https://www.wanted.co.kr"

            title_tag = job_card.find("strong", class_="JobCard_title__HBpZf")
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"

            company_name_tag = job_card.find("span", class_="JobCard_companyName__N1YrF")
            company_name = company_name_tag.get_text(strip=True) if company_name_tag else "회사명 없음"

            detail_url_tag = job_card.find("a", href=True)
            detail_url = base_url + detail_url_tag['href'] if detail_url_tag else "URL 없음"

            job_data = {
                "title": title,
                "company_name": company_name,
                "detail_url": detail_url,
                "platform_name": "wanted"
            }

            additional_info = self.scrape_additional_info(job_data["detail_url"])
            job_data.update(additional_info)

            self.request_save(job_data)  # 스크래핑한 데이터를 저장하는 메서드 호출

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(process_job, job_card) for job_card in job_cards]
            for future in as_completed(futures):
                jobs_data.append(future.result())

        driver.quit()

class JobplanetScraper(BaseScraper): # jk
    def __init__(self):
        super().__init__()
    
    # 크롤링을 수행하는 scrap() 메서드
    def scrap(self):
        # 추가 정보를 스크래핑하는 함수
        def scrape_additional_info(url):
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(url)
            time.sleep(3)  # 페이지 로딩 대기

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # 마감일 추출 (end_date)
            end_date_element = soup.find("span", class_="recruitment-summary__end")
            end_date = end_date_element.get_text(strip=True) if end_date_element else None

            # 경력 추출 (career)
            career_element = None
            for dt in soup.find_all("dt", class_="recruitment-summary__dt"):
                if "경력" in dt.get_text(strip=True):
                    career_element = dt.find_next_sibling("dd")
                    break
            career = career_element.get_text(strip=True) if career_element else None

            # 지역 추출 (region)
            region_element = soup.find("span", class_="recruitment-summary__location")
            region = region_element.get_text(strip=True) if region_element else None

            # 기술 스택 추출 (stack)
            stack_element = None
            for dt in soup.find_all("dt", class_="recruitment-summary__dt"):
                if "스킬" in dt.get_text(strip=True):
                    stack_element = dt.find_next_sibling("dd")
                    break
            stack = [tech.strip() for tech in stack_element.get_text(strip=True).split(",")] if stack_element else []

            driver.quit()
            return {
                "end_date": end_date,
                "career": career,
                "region": region,
                "stack": stack
            }

        # 메인 크롤링 작업 시작
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
            driver.get("https://www.jobplanet.co.kr/welcome/index/")
            driver.implicitly_wait(5)

            # 채용 버튼 클릭
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "job_posting"))
            )
            ActionChains(driver).click(button).perform()

            # 직종 버튼 클릭
            job_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '직종')]"))
            )
            ActionChains(driver).click(job_button).perform()

            # 데이터 버튼 클릭
            data_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='데이터']"))
            )
            ActionChains(driver).click(data_button).perform()

            # 데이터 전체 버튼 클릭
            engineer_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='데이터 전체']"))
            )
            ActionChains(driver).click(engineer_button).perform()

            # 적용 버튼 클릭
            apply_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='적용']"))
            )
            ActionChains(driver).click(apply_button).perform()

            # 스크롤 작업 시작
            time.sleep(10)
            scroll_pause_time = 1
            scroll_limit = 1

            for _ in range(scroll_limit):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)

            # BeautifulSoup으로 페이지 파싱
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # 1. a 태그에서 href 속성을 추출
            links = soup.find_all("a", "group z-0 block medium", title="페이지 이동")

            # 2. 공고 정보 추출
            job_elements = soup.find_all("div", "group mt-[16px] group-[.small]:mt-[14px] medium")

            # 3. 멀티스레딩으로 각 공고의 추가 정보를 병렬로 스크래핑
            def process_job(job, link):
                job_data = {}

                title = job.find("h2", "line-clamp-2 break-all text-h7 text-gray-800 group-[.small]:text-h8")
                job_data["title"] = title.get_text(strip=True) if title else None

                company_name = job.find("em", "inline-block w-full truncate text-body2 font-medium text-gray-800")
                job_data["company_name"] = company_name.get_text(strip=True) if company_name else None

                job_data["detail_url"] = link.get("href")
                job_data["platform_name"] = "Jobplanet"

                # 추가 정보를 가져오기
                additional_info = scrape_additional_info(job_data["detail_url"])
                job_data.update(additional_info)

                # 스크래핑 결과를 request_save로 저장
                self.request_save(job_data)

            # 스레드 풀을 사용하여 병렬 처리
            with ThreadPoolExecutor(max_workers=7) as executor:
                futures = [executor.submit(process_job, job, link) for job, link in zip(job_elements, links)]
                for future in as_completed(futures):
                    future.result()  # 결과를 처리

class ProgrammersScraper(BaseScraper):

    def __init__(self):
        super().__init__()
        self.search_querys = ['데이터'] 

    def scrap(self):
        search_querys = self.search_querys

        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:  
            for keyword in search_querys:
                url = "https://career.programmers.co.kr/job?page=1&order=recent&job_category_ids=5&job_category_ids=11&job_category_ids=12&job_category_ids=92/?search_query={}".format(keyword)
                driver.get(url)

                while True:
                    try:
                        # 각 페이지가 완전히 로드될 때까지 대기
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#list-positions-wrapper > ul > li"))
                        )
                    except Exception as e:
                        print(f"Error extracting element data: {e}")
                        break

                    # BeautifulSoup으로 페이지 파싱
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    job_element = soup.select("#list-positions-wrapper > ul > li") # 페이지의 모든 공고 탐색

                    # 각 공고의 정보 추출
                    for element in job_element:
                        try:
                            company_name = element.select_one("h6.company-name > a")
                            title_tag = element.select_one("h5.position-title > a")
                            link_tag = element.select_one("a.company-link")
                            tech_stack_elements = element.select("ul.list-position-tags > li")
                            career_tag = element.select_one("li.experience")
                            region_tag = element.select_one("li.location")

                            job_info = {
                                "title": title_tag.get_text(strip=True) if title_tag else "제목 없음",
                                "company_name": company_name.get_text(strip=True) if company_name else "회사명 없음",
                                "detail_url": "https://career.programmers.co.kr" + link_tag["href"] if link_tag else "링크 없음",
                                "end_date": None, # 마감일 정보 없음
                                "platform_name": "programmers",
                                "category_name": None,  # 카테고리 정보 없음
                                "stack": [el.get_text(strip=True) for el in tech_stack_elements] if tech_stack_elements else None,
                                "region": region_tag.get_text(strip=True) if region_tag else "지역 없음",
                                "career": career_tag.get_text(strip=True) if career_tag else "경력/신입 없음"
                            }

                            # 요청 1개씩 바로바로 보내기
                            self.request_save(job_info)
                        except Exception as e:
                            print(f"Error extracting element data: {e}")

                    # 다음 페이지 버튼 탐색 및 클릭 (텍스트 '>' 활용)
                    try:
                        next_button = driver.find_element(By.XPATH, '//span[@class="page-link" and text()=">"]')
                        next_button.click()
                        time.sleep(2)  # 페이지 로딩 대기
                    except Exception as e:
                        print(f"No more pages or error navigating: {e}")
                        break  # 더 이상 페이지가 없으면 종료

        self.request_save(job_info)
        pass

class CatchScraper(BaseScraper):

    def __init__(self):
        super().__init__()
    def scrap(self):
        # Selenium으로 브라우저 열기
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
            # 현재 연도를 가져오기
            current_year = datetime.now().year
            # 페이지 순회 (1페이지만 수집)
            url = "https://www.catch.co.kr/NCS/RecruitSearch?page=1"  # 검색 키워드를 URL에 추가하지 않음
            driver.get(url)
            try:
                # 특정 요소가 나타날 때까지 기다림
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'tr td p.date'))
                )
            except Exception as e:
                print(f"요소를 찾을 수 없습니다: {e}")
                return  # 크롤링 중단
            # page_source로 페이지의 HTML 가져오기
            html = driver.page_source
            # BeautifulSoup을 사용해 HTML 파싱
            soup = BeautifulSoup(html, 'html.parser')
            # 회사명 추출
            company_names = soup.select('tr td.al1 p.name')
            # 공고문 제목 추출
            job_titles = soup.select('tr td a.link')
            # 마감일 추출
            end_dates = soup.select('tr td p.date')
            # 결과 저장 및 출력
            for company, title, date in zip(company_names, job_titles, end_dates):
                # 마감일에서 "~" 이후의 날짜만 추출
                full_date_text = date.get_text().strip()
                if "~" in full_date_text:
                    end_date_str = full_date_text.split("~")[-1].strip()  # "~" 이후의 날짜만 추출
                else:
                    end_date_str = full_date_text  # "~"가 없는 경우 전체 날짜 사용
                # 현재 연도 추가 후 날짜 형식 변환
                try:
                    end_date_with_year = f"{current_year}.{end_date_str}"
                    end_date = datetime.strptime(end_date_with_year, '%Y-%m-%d').strftime('%y-%m-%d')
                except ValueError:
                    end_date = end_date_str  # 형식 변환 실패 시 원본 유지
                # 상세 URL 추출 (job_titles에서 href 가져오기)
                detail_url = title['href']  # title 객체에서 href 속성 가져오기
                detail_url = "https://www.catch.co.kr" + detail_url  # 전체 URL 형식으로 변환
                # 요청 1개씩 바로바로 보내기
                job_info = {
                    "title": title.get_text().strip(),  # 공고 제목
                    "company_name": company.get_text().strip(),  # 회사 이름
                    "detail_url": detail_url,  # 디테일 페이지 URL
                    "end_date": end_date,  # 마감일 (현재 연도 포함)
                    "platform_name": "Catch"  # 플랫폼 이름
                }
                self.request_save(job_info)  # 요청을 보내기                

class PeoplenJobScraper(BaseScraper):

    def __init__(self):
        super().__init__()  # 부모 클래스(BaseScraper)의 생성자 호출
    def scrap(self):
        # 크롤링할 데이터를 저장할 리스트 (개별적으로 보내는 대신 리스트로 관리 가능)
        jobs = []
        # Selenium을 이용해 Chrome 브라우저 실행
        with webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="129.0.6668.101").install())) as driver:
            page = 1  # 페이지 번호 초기값 설정
            while True:
                url = f'https://www.peoplenjob.com/jobs?field=all&q=데이터&page={page}'
                driver.get(url)  # 해당 URL로 이동
                time.sleep(2)  # 페이지 로딩을 위해 잠시 대기 (2초)
                # 페이지 소스를 BeautifulSoup으로 분석
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # 각 공고가 담긴 테이블 행 (tr) 태그 찾기
                rows = soup.find_all('tr')
                # 각 공고에서 필요한 정보 추출 및 리스트에 추가
                for row in rows:
                    try:
                        # 공고 제목
                        title_tag = row.find('td', class_='job-title')
                        title = title_tag.find('a').text.strip() if title_tag else 'N/A'
                        # 회사 이름
                        company_tag = row.find('td', class_='name')
                        company_name = company_tag.find('a').text.strip() if company_tag else 'N/A'
                        # 상세 페이지 URL
                        detail_url_tag = title_tag.find('a') if title_tag else None
                        detail_url = f"{detail_url_tag['href']}" if detail_url_tag else 'N/A'
                        # 마감일
                        end_date_tag = row.find('span', class_='job-fin-date')
                        end_date = end_date_tag.text.strip() if end_date_tag else 'N/A'
                        # 카테고리 (직무 타입)
                        category_tag = row.find('td', class_='job_type')
                        category_name = category_tag.text.strip() if category_tag else 'N/A'
                        # 기술 스택 (이 사이트에는 없으므로 'N/A'로 처리)
                        stack = 'N/A'
                        # 모든 <td> 태그를 리스트로 가져옴
                        td_tags = row.find_all('td')
                        # <td> 태그가 최소한 2개 이상 있는지 확인
                        if len(td_tags) >= 2:
                            region_tag = td_tags[-2].find('a')  # 두 번째 마지막 <td>에서 <a> 태그 찾기
                            region = region_tag.text.strip() if region_tag else 'N/A'
                        else:
                            region = 'N/A'  # <td> 태그가 2개 미만인 경우 N/A로 설정
                        # 신입/경력 (이 사이트에는 없으므로 'N/A'로 처리)
                        career = 'N/A'
                        # 출처 (플랫폼 이름)
                        platform_name = 'peoplenjob'
                        # 추출한 데이터를 딕셔너리로 추가
                        job_data = {
                            'title': title,
                            'company_name': company_name,
                            'detail_url': detail_url,
                            'end_date': end_date,
                            'platform_name': platform_name,
                            'category_name': category_name,
                            'stack': stack,
                            'region': region,
                            'career': career
                        }
                        # 개별적으로 데이터 서버에 요청 보내기
                        self.request_save(job_data)
                    except Exception as e:
                        print(f"Error parsing job: {e}")
                print(f"{page} 페이지 크롤링 완료")
                # '다음' 버튼이 비활성화된 경우 크롤링 종료
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "li.next.disabled")
                    if next_button:
                        print("마지막 페이지에 도달하여 크롤링을 종료합니다.")
                        break
                except:
                    pass  # 다음 버튼이 활성화되어 있다면 크롤링 계속
                page += 1  # 다음 페이지로 이동
    def start(self):
        # 스케줄러를 60초 간격으로 설정하고 크롤링 작업 시작
        self.start_scraper_scheduler(interval_seconds=60)
    def stop(self):
        # 스케줄러 중지
        self.stop_scraper_scheduler()


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


    def __init__(self):
        super().__init__()
        self.search_querys = ["데이터분석", "데이터 엔지니어", "데이터 사이언티스트"] 
        self.keyword_index = 0   
    
    def parse_end_date(self, date_text):
        if "오늘마감" in date_text:
            return datetime.now().strftime("%Y-%m-%d")
        if "내일마감" in date_text:
            return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        if date_text.startswith("~ "):
            date_text = date_text[2:]
            try:
                current_year = datetime.now().year
                date_obj = datetime.strptime(f"{current_year}/{date_text[:5]}", "%Y/%m/%d")
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

class IncruitScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.all_jobs = []

    # 지역명 정리
    def clean_region_name(self, region):
        cleaned_region = re.sub(r'\s외.*$', '', region)
        return cleaned_region

    # 경력 정리
    def clean_career(self, career):
        if '신입' in career:
            return '신입'
        return career

    # 마감일 변환
    def convert_end_date(self, end_date):
        today = datetime.now()

        # "23시 마감" 형식 처리
        if "마감" in end_date:
            return today.strftime('%Y-%m-%d')

        # "~10.21 (월)" 형식 처리
        match = re.search(r'~(\d{1,2})\.(\d{1,2})', end_date)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            return today.replace(month=month, day=day).strftime('%Y-%m-%d')

        # 다른 형식은 그대로 반환
        return end_date
    
    def scrap(self):
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
            url = 'https://job.incruit.com/jobdb_list/searchjob.asp?occ3=16935&occ3=16501&occ3=16182&occ3=14780&occ3=17030&occ3=16895&occ3=16865&occ3=16761&occ3=16903&occ2=632&page=1'
            driver.get(url)
            time.sleep(3)
            page_num = 1  # 페이지 번호를 추적하기 위한 변수 추가
            while True:
                print(f"현재 {page_num} 페이지 크롤링 중입니다.")
                jobs = driver.find_elements(By.CLASS_NAME, 'c_col')

                for job in jobs:
                    try:
                        company_name = job.find_element(By.CLASS_NAME, 'cell_first').find_element(By.TAG_NAME, 'a').text
                        mid = job.find_element(By.CLASS_NAME, 'cell_mid')
                        title = mid.find_element(By.TAG_NAME, 'a').text
                        detail_url = mid.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        spans = mid.find_elements(By.TAG_NAME, 'span')

                        filtered_spans = [span for span in spans if 'highlight' not in span.get_attribute('class')]

                        if len(filtered_spans) > 2:
                            region = filtered_spans[2].text
                        else:
                            region = ""
                        if len(filtered_spans) > 0:
                            career = filtered_spans[0].text
                        else:
                            career = ""
                        end_date = job.find_element(By.CLASS_NAME, 'cell_last').find_element(By.CLASS_NAME, 'cl_btm').find_element(By.TAG_NAME, 'span').text

                        job_info = {
                            "title": title,
                            "company_name": company_name,
                            "detail_url": detail_url,
                            "end_date": self.convert_end_date(end_date),
                            "platform_name": "incruit",
                            "category_name": "",  
                            "stack": "",  
                            "region": self.clean_region_name(region),
                            "career": self.clean_career(career)
                        }
                        self.request_save(job_info)

                    except Exception as e:
                        print(f"Error extracting job data: {e}")
                