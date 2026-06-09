from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import pandas as pd
import random
import time

# 경고 무시
import warnings
warnings.filterwarnings('ignore')


"""키워드로 네이버 뉴스 검색하여 크롤링하기"""

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox') # 보안 기능인 샌드박스 비활성화
options.add_argument('--disable-dev-shm-usage') # dev/shm 디렉토리 사용 안함
options.add_argument("--start-maximized") # 화면 최대 크기로 설정
options.add_experimental_option("useAutomationExtension", False)  # 자동화 확장기능 비활성화
options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 탐지 회피

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


keyword = '젠슨황'

driver.get('https://www.naver.com/')
driver.implicitly_wait(5) #로딩하는 시간 최대 5초 기다림, 로딩 되면 바로 끝

# 사람인 척
time.sleep(random.uniform(2,4))

# 검색창 찾아 search_box 변수에 저장하기
search_box = driver.find_element(By.ID, 'query')

search_box.send_keys(keyword) # 검색창에 키워드 입력
search_box.send_keys(Keys.RETURN) # 엔터키 누르기
 
time.sleep(1)
driver.find_element(By.LINK_TEXT, "뉴스").click() # 뉴스탭 클릭
time.sleep(random.uniform(2,3))


# 스크롤 내리면서 기사 수집하기
last_height = driver.execute_script(
    "return document.documentElement.scrollHeight"
)

for i in range(20):  # 스크롤은 20번만 내릴 거에요.
    print(f"{i+1}번째 스크롤")

    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    time.sleep(random.uniform(2,4))

    new_height = driver.execute_script("return document.documentElement.scrollHeight")

    # 목표한 스크롤 횟수를 채우지 않아도 더 스크롤할 기사가 없으면 종료
    if new_height == last_height:
        time.sleep(3)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            print("더는 기사가 없습니다.")
            break

    last_height = new_height


# 느려터진 셀레니움 대신 BeautifulSoup로 HTML 파싱 
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

news_cards = soup.select(".sds-comps-vertical-layout.sds-comps-full-layout")

seen_links = set()
news_data = []

for card in news_cards:

    press_tag = card.select_one(".sds-comps-profile-info-title-text")

    title_tag = card.select_one('a[data-heatmap-target=".tit"]')

    summary_tag = card.select_one(".sds-comps-text-ellipsis-3")

    if not title_tag:
        continue

    link = title_tag.get("href")

    # 이미 수집한 기사면 건너뛰기
    if link in seen_links:
        continue

    seen_links.add(link)

    news_data.append({
        "언론사": press_tag.get_text(strip=True)
                if press_tag else "",
        "제목": title_tag.get_text(strip=True),
        "요약": summary_tag.get_text(strip=True)
                if summary_tag else "",
        "링크": link
    })

news_df = pd.DataFrame(news_data)

print(news_df.info())
news_df.to_csv(f'{keyword}_news.csv', encoding='utf-8-sig', index=False)
driver.quit()
