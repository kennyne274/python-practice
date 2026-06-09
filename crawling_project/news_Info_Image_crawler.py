import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 

"""중앙일보 홈페이지에서 키워드로 검색한 기사의 정보를 정해진 페이지 만큼 수집합니다.
제목, url, 날짜, 요약문 수집. 이미지는 내 폴더에 다운로드""" 

os.makedirs("new_img", exist_ok=True) # 뉴스 이미지를 저장할 폴더 생성

data = []

keyword ="만두" # 키워드는 원하는 대로
page_num = 2

headers = {'User-Agent' : 'Mozilla/5.0'}


for i in range(1, page_num+1):
    url = f'https://www.joongang.co.kr/search/news?keyword={keyword}&page={i}' 

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_list = soup.select("li.card")
    news_list

    for j, news in enumerate(news_list, start=1):
        try:
            """제목, url, 언론사, 날짜, 이미지 수집"""
            title = news.select_one("h2.headline a").get_text(strip=True)
            link = news.select_one("h2.headline a").attrs["href"]
            press = news.select_one("p.source").get_text()
            date = news.select_one("p.date").get_text()
            
            # 이미지를 수집하고 내 폴더에 다운로드 받기
            img_tag = news.select_one("img")   
            if img_tag:

                img = img_tag["src"]
                img_data = requests.get(img).content

                with open(f"new_img/image_{i}_{j}.jpg","wb") as f:

                    f.write(img_data)
            #===============================================

            print("제목 :", title)
            print("주소 : ", link)
            print("언론사: ", press)
            print("날짜 :", date)
            print()
            data.append([press, title, link, date])
        
        except Exception:
            pass

df = pd.DataFrame(data, columns=["신문사", "제목", "기사 링크", "날짜"])
df.to_excel("중앙일보크롤링2.xlsx", index=False)
df.to_csv("네이버뉴스크롤링.csv", index=False, encoding="utf-8-sig") # csv로 저장
