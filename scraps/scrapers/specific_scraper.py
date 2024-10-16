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
        data_list = []
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:  
            for keword in search_querys:
                url = "https://www.theteams.kr/results/recruit/?search_query={}".format(keword)
                driver.get(url)

                while True:
                    # 현재 URL 출력
                    # print(f"Current URL: {driver.current_url}")
                    # 캡션 클래스 내부에 data를 수집
                    elements = driver.find_elements(By.CLASS_NAME, "caption")
                    for element in driver.find_elements(By.CLASS_NAME, "caption"):
                        try:
                            category_element = element.find_element(By.CLASS_NAME, "badge_occupation") #카테고리 이름, ex)데이터 사이언스
                            carrer_element = element.find_elements(By.TAG_NAME, "div")[1] #carrer, ex)신입/경력 
                            title_element = element.find_element(By.TAG_NAME, "h4") #공고제목, ex) [숨고] Business Data Analyst
                            company_nm_element = element.find_element(By.TAG_NAME, "p") #회사이름, ex) (주)브레이브모바일
                            detial_url_element = element.find_element(By.TAG_NAME, "a") #디테일 페이지 주소
                            

                            job_info = {
                                        "title": title_element.text.strip(),
                                        "company_name": company_nm_element.text.strip(),
                                        "detail_url": detial_url_element.get_attribute("href"),
                                        "end_date": "수시채용",
                                        "platform_name": "theteams",
                                        "category_name": category_element.text.strip(),
                                        "stack": "기술스택",
                                        "region": "지역",
                                        "career": carrer_element.text.strip(),
                            }
                            data_list.append(job_info)
                            # print("Text:", (div_element.text.strip(), h4_element.text.strip(), p4_element.text.strip(), a4_element))
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
        self.request_save(data_list)
