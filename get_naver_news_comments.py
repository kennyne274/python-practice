from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup 
import random
import time
import pandas as pd


# 네이버 기사에서 댓글 수집하여 저장하기


# 경고 발생하면 무시.
import warnings 
warnings.filterwarnings('ignore')

options = Options()
options.add_argument("--start-maximized") # 화면을 제일 크게 시작
options.add_experimental_option("detach", True) # 화면이 바로 꺼지지 않도록
options.add_experimental_option("useAutomationExtension", False)  # 자동화 확장기능 비활성화
options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 탐지 회피


# 네이버 뉴스 댓글 정보 수집 함수
def get_naver_news_comments(url):
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    driver.implicitly_wait(5) #로딩하는 시간 5초 기다림, 로딩 되면 바로 끝


    while True:
         # 현재 화면에 로딩된 댓글 개수 확인
        comments = driver.find_elements(By.CSS_SELECTOR,"span.u_cbox_contents")

        # 더보기 버튼을 누르기 전 댓글 개수 저장
        prev_count = len(comments)

        try:
            # "더보기" 버튼 찾기
            more_btn = driver.find_element(By.CSS_SELECTOR,"a.u_cbox_btn_more")

            # 더보기 버튼이 화면에 보이도록 스크롤 이동
            driver.execute_script("arguments[0].scrollIntoView();", more_btn)

            # 사람이 읽고 클릭하는 것처럼 잠시 대기
            time.sleep(random.uniform(1.5, 3))

            # JavaScript로 더보기 버튼 클릭
            driver.execute_script("arguments[0].click();",more_btn)

            time.sleep(random.uniform(2, 3))

            # 클릭 후 댓글 개수 다시 확인
            comments = driver.find_elements(By.CSS_SELECTOR,"span.u_cbox_contents")

            current_count = len(comments)
            
            # 더 이상 가져올 댓글이 없으면 종료
            if current_count == prev_count:
                break

        # 더 보기 없으면 마지막 페이지에 도달한 것으로 간주하고 반복문을 나감
        except:
            break

    # HTML 가져오기
    html = driver.page_source

    # 파싱
    soup = BeautifulSoup(html, "html.parser")

    # 1) 작성자
    nicknames = soup.select('span.u_cbox_nick')
    list_nicknames = [nickname.text for nickname in nicknames]

    # 2)댓글 시간
    datetimes = soup.select('span.u_cbox_date')
    list_datetimes = [datetime.text for datetime in datetimes]

    # 3)댓글 추출
    comments = soup.select("span.u_cbox_contents")
    list_contents = [
    content.get_text(strip=True)
    for content in comments
    ]

    print(f"댓글 수 : {len(comments)}")

    for idx, comment in enumerate(comments, start=1):
        print(f"[{idx}] {comment.get_text(strip=True)}")
    
    # 작성자, 댓글 시간, 내용을 셋트로 취합
    list_sum = list(zip(list_nicknames,list_datetimes,list_contents))

    # 드라이버 종료
    driver.quit()

    # 함수를 종료하며 list_sum을 결과물로 제출
    return list_sum


# 메인 실행 구간
if __name__ == '__main__':
        
        # 댓글 수집할 기사 url
        # url = "https://n.news.naver.com/article/comment/016/0002651674"
        url = 'https://n.news.naver.com/article/comment/005/0001853121'

        news_comments = get_naver_news_comments(url)

        # 엑셀의 첫줄에 들어갈 컬럼명
        col = ['작성자','시간','내용']

        # pandas 데이터 프레임 형태로 가공
        df = pd.DataFrame(news_comments, columns=col)

        # csv로 저장
        df.to_csv(f'news_comments.csv',
                        encoding='utf-8-sig',
                        index=False)
