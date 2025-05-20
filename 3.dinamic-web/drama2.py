from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

drama = []

# 크롬 드라이버 설정
driver = webdriver.Chrome()
URL = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%EB%B0%A9%EC%98%81%EC%A2%85%EB%A3%8C%ED%95%9C%EA%B5%AD%EB%93%9C%EB%9D%BC%EB%A7%88'
driver.get(URL)

# 페이지 로딩을 기다림
try:
    # 예시로 드라마 목록이 있는 요소가 로드되기를 기다림
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.info_box>strong>a')))
    
    # 드라마 이름과 시청률 크롤링
    names = driver.find_elements(By.CSS_SELECTOR, 'li.info_box>strong>a')
    ratings = driver.find_elements(By.CSS_SELECTOR, 'li.info_box>div.sub_info>span>span>em')

    for i in range(len(names)):
        name = names[i].text
        rating = ratings[i].text
        drama.append([name, rating])

finally:
    driver.quit()

print(drama)