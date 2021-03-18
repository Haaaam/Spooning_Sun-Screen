import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from urllib.request import urlopen
from urllib.parse import quote
import time
import re
import platform
import csv


keyword=input("검색어 입력: ")
start_date=input("조회를 시작할 날짜를 입력하세요(예:20210101): ")
end_date=input("조회를 종료할 날짜를 입력하세요(예:20210101): ")
END_PAGE=int(input("마지막 페이지를 입력하세요: "))+1
url="https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword="+keyword


driver=webdriver.Chrome("d:/py_data/chromedriver.exe")



driver.implicitly_wait(5)
driver.get(url)
time.sleep(3)


html=driver.page_source
soup=bs(html,'html.parser')


url1="https://section.blog.naver.com/Search/Post.nhn?pageNo="
url2="&rangeType=PERIOD&orderBy=sim&startDate=2016-01-01&endDate=2021-03-18&keyword="+keyword
driver.implicitly_wait(10)

date_lst=[]
cnt=0
for now_page in range(1,END_PAGE):
    driver.get(url1+str(now_page)+url2)
    time.sleep(2)
    html=driver.page_source
    soup=bs(html,'html.parser')
    div_lst=soup.find_all('div',class_='list_search_post')
    ww=soup.find('div',class_="search_information")
    total=int(ww.find('em',class_="search_number").text.replace(',','').replace('건',''))

    for i in range(len(div_lst)):
        cnt+=1
        try:
            date=int(div_lst[i].find('span',class_='date').text.replace('. ','').replace('.','')[:4])
            date_lst.append(date)
        except:
            pass
        if cnt==total:
            break
    if cnt==total:
        break

driver.close()


df=pd.DataFrame({"date":date_lst})
df.to_csv('d:/py_data/'+keyword+'.csv',encoding='cp949')
