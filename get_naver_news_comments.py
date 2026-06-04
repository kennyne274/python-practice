# 네이버 뉴스 댓글 수집

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup 
import random
import time
import pandas as pd


def get_naver_news_comments(url):
    options = Options()
    options.add_argument("--start-maximized") # 화면을 제일 크게 시작
    options.add_experimental_option("detach", True) # 화면이 바로 꺼지지 않도록
    options.add_experimental_option("useAutomationExtension", False)  # 자동화 확장기능 비활성화
    options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 탐지 회피

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        driver.implicitly_wait(5)
        time.sleep(3)

        while True:
            comments = driver.find_elements(By.CSS_SELECTOR, "span.u_cbox_contents")
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

        return list_sum

    except Exception as e:
        print(f"오류 발생: {e}")
        return None

    finally:
        driver.quit()   # 드라이버 종료


# 메인 실행
if __name__ == '__main__':

    url = 'https://n.news.naver.com/article/comment/005/0001853121'

    news_comments = get_naver_news_comments(url)

    col = ['작성자','시간','내용']

    # pandas 데이터 프레임 형태로 가공
    if news_comments:
        df = pd.DataFrame(news_comments, columns=col)
        df.to_csv(f'news_comments.csv', # csv로 저장
                        encoding='utf-8-sig',
                        index=False)
        print("CSV 파일로 저장 완료!")
        print(df.head())
    else:
        print("댓글 수집에 실패했습니다.")
        
