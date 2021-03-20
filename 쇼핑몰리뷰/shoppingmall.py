from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from tqdm.notebook import tqdm
import re
import sys
import time

url="https://search.shopping.naver.com/catalog/22763470633?query=%EC%9C%A0%EC%95%84%EC%8D%AC%ED%81%AC%EB%A6%BC&NaPm=ct%3Dkmghgx3s%7Cci%3D6b8ca8746208bb44b5f49ab151649efe6665142c%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D97bec0ba0fb498f36705a63d2720abacdd3517f4"
driver=webdriver.Chrome("d:/py_data/chromedriver.exe")
driver.get(url)
time.sleep(2)

html=driver.page_source
soup=BeautifulSoup(html,"html.parser")
menu_area=soup.find('div',class_='floatingTab_detail_tab__2T3U7').find_all('strong')
review_num=0
for i in range(len(menu_area)):
    menu=menu_area[i].text
    if menu=='쇼핑몰리뷰':
        driver.find_element_by_css_selector("#snb > ul > li.floatingTab_on__299Bi > a").click()
        review_num=int(soup.find('div',class_='floatingTab_detail_tab__2T3U7').find_all('a')[i].find('em').text.replace(',',''))

        break

next_btn_element = '#section_review > div.pagination_pagination__2M9a4 > '
next_btn = ['a:nth-child(2)','a:nth-child(3)',
            'a:nth-child(4)','a:nth-child(5)',
            'a:nth-child(6)','a:nth-child(7)',
            'a:nth-child(8)','a:nth-child(9)',
            'a:nth-child(10)','a.pagination_next__3ycRH']

point_lst = []
doc_lst = []
now_page = 0
for page in range((review_num // 20) + 1):
    #    for rnum in next_btn:
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    review_area = soup.find_all('div', class_='reviewItems_review__1eF8A')

    # 리뷰 더보기 클릭
    for num in range(1, len(review_area) + 1):
        try:
            driver.find_element_by_css_selector(
                '#section_review > ul > li:nth-child(' + str(num) + ') > div.reviewItems_btn_area__2St26 > a').click()
            time.sleep(1)
        except:
            pass

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    point_area = soup.find_all('span', class_='reviewItems_average__16Ya-')
    try:
        point_area = soup.find_all('span', class_='reviewItems_average__16Ya-')
    except:
        break
    for i in point_area:
        point_lst.append(int(i.text.replace('평점', '')))

    review_area = soup.find_all('div', class_='reviewItems_review__1eF8A')
    for i in review_area:
        doc_lst.append(re.sub('[^a-zA-Zㄱ-ㅣ가-힣0-9?!# ]', "", i.text))
    driver.find_element_by_css_selector(next_btn_element + next_btn[now_page]).click()
    now_page = now_page + 1
    time.sleep(1)

    if next_btn[now_page] == 'a.pagination_next__3ycRH':
        next_btn = ['a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)',
                    'a:nth-child(8)', 'a:nth-child(9)', 'a:nth-child(10)', 'a:nth-child(11)',
                    'a:nth-child(12)', 'a.pagination_next__3ycRH']
        now_page = 0

df = pd.DataFrame({"평점": point_lst, "본문": doc_lst})
df.to_csv("./data/아토보스 인리치드 무기자차 선크림.csv", encoding="cp949")
print(len(point_lst), '개의 게시물을 크롤링 하였습니다.')
driver.close()