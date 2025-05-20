from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import csv

local_file_path = '/home/ubuntu/damf2/nielsen/data/tv1/'

def save_to_csv(data, date): 
    file_date = f"{date}.csv"
    with open(local_file_path + file_date, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

driver = webdriver.Chrome()

# 지상파/ 종편/ 케이블 링크 변경 필요
URL = 'https://www.nielsenkorea.co.kr/tv_terrestrial_day.asp?menu=Tit_1&sub_menu=1_1&area=01'
driver.get(URL)

# 2024 or 2025
year = driver.find_element(By.CSS_SELECTOR, '#select > option[value="2025"]')
year.click()

# 2025 상반기 => 01, 02, 03 / 2024 하반기 => 07, 08, 09, 10, 11, 12
month = driver.find_element(By.CSS_SELECTOR, '#select2 > option[value="01"]')
month.click()

# 1, 3, 7, 8, 10, 12월 => range 32까지 / 9, 11월 => range 31까지 / 2월 => range 29까지
for i in range(1, 32):
    if i < 10:
        day = driver.find_element(By.CSS_SELECTOR, f'#select1 > option[value="0{i}"]')
        day.click()    
    else:
        day = driver.find_element(By.CSS_SELECTOR, f'#select1 > option[value="{i}"]')
        day.click()

    # 서치 버튼 클릭
    search_button = driver.find_element(By.CSS_SELECTOR, 'img[onclick="goSearch();"]')
    search_button.click()

    # 데이터 쪼개기
    td_list = driver.find_elements(By.CSS_SELECTOR, 'td')
    td_texts = [td.text for td in td_list]
    result = []
    for text in td_texts:
        result.append(text)

    # print(result)

    print(result[13]) # 날짜

    rlist = result[14].split('\n') # 시청률 데이터 줄별로 쪼개기

    answer = []
    # 띄어쓰기 기준으로 스플릿해야하므로 채널명에 띄어쓰기가 있는 경우 없애기
    exceptions = [
    "TV CHOSUN", "SBS Plus", "KBS Drama", "KBS JOY", "MBC every1",
    "MBC SPORTS+", "SBS Sports", "KBS N 스포츠", "EBS 플러스", "EBS English",
    "EBS 키즈", "National Geographic", "Discovery Channel", "Channel CGV",
    "JEI 재능TV", "대교 어린이TV", "tvN STORY", "SPOTV Prime"
]

    # 데이터 리스트에 넣기
    for r in rlist:
        for ex in exceptions:
            r = r.replace(ex, ex.replace(" ", ""))
        r = r.split(' ')
        answer.append(r)
    print(answer[3:])

    # 데이터 저장
    save_to_csv(answer[3:], result[13])