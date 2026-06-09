import requests
from bs4 import BeautifulSoup
import pandas as pd

# 네이버 뉴스란에서 10개의 기사 정보를 수집합니다.
# 수집하는 r기사 정보는 언론사, 제목, 요약, 본문, 날짜, url
# 수집한 정보는 데이터프레임으로 변환 후 엑셀과 csv파일로 저장

code = 105 # it/과학 뉴스, 수집할 기사의 종류는 원하는 대로 설정하세요
number = 10 # 수집할 기사 갯수

data= [] # 수집한 기사 정보를 담을 빈 리스트 생성

news_url = f'https://news.naver.com/section/{code}' 

headers = {"User-Agent": "Mozilla/5.0"}

def crawl_news(url, num):
    """언론사, 제목, 요약, 링크 주소를 수집 후 판다스로 엑셀에 저장"""
    count = 0
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # 기사 목록 가져오기
        news_list = soup.select("li.sa_item")
        for i, news in enumerate(news_list, start=1):
            if count >= num: 
                break

            try:
                # 언론사
                press = news.select_one("div.sa_text_press").get_text()
                # 제목
                title_tag = news.select_one("a.sa_text_title")
                title = title_tag.get_text(strip=True)
                # url 주소
                link = title_tag["href"]
                # 요약본
                summary_tag = news.select_one("div.sa_text_lede")
                summary = (
                    summary_tag.get_text(strip=True)
                    if summary_tag else ""
                )
                                # 본문, 날짜
                content, time = news_text(link)
        
                count += 1

                print(f"[{i}]")
                print("신문사 :", press)
                print("제목 :", title)
                print("요약 :", summary)
                print("주소 :", link)
                print("기사 본문 : ", content)   
                print("날짜 :", time)            
                print("-" * 50)

                data.append([press, title, summary, link, content, time])             
            
            except:
                pass

    else:
        print(f'페이지 요청 실패 {response.status_code}')

def news_text(url):
    """기사 본문과 날짜 수집"""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # 기사 목록 가져오기
        date_time = soup.select_one("div.media_end_head_info_datestamp").get_text(strip=True).replace('기사원문','')
        news_text = soup.select_one("div#newsct_article").get_text(strip=True)      
        return news_text, date_time


# 실행 구간
if __name__ == '__main__':
    crawl_news(news_url ,number)

    # 크롤링한 뉴스를 엑셀과 csv파일로 저장하기
    df = pd.DataFrame(data, columns=["신문사", "제목", "요약", "주소", "본문", "날짜"])
    df.to_excel(f"naver_news{code}.xlsx", index=False)
    df.to_csv(f"naver_news{code}.csv", index=False, encoding="utf-8-sig") # csv로 저장

