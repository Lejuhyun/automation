from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

drama = []

driver = webdriver.Chrome()
URL = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%EB%B0%A9%EC%98%81%EC%A2%85%EB%A3%8C%ED%95%9C%EA%B5%AD%EB%93%9C%EB%9D%BC%EB%A7%88'
driver.get(URL)

# 년도 변경
year_btn = driver.find_element(By.CSS_SELECTOR, 'li[data-key="year"]')
target_btn = year_btn.find_element(By.CSS_SELECTOR, 'a')
target_btn.click()

# 하위 드롭다운목록에서 특정 년도 선택
target_year_btn = driver.find_element(By.CSS_SELECTOR, 'ul.list_item > li.item._item[data-value="2023"] > a')
target_year_btn.click()
time.sleep(2)

# 지상파
broadcast_btn = driver.find_element(By.CSS_SELECTOR, 'li[data-key="broadcast"]')
target_btn_2 = broadcast_btn.find_element(By.CSS_SELECTOR, 'a')
target_btn_2.click()

# 하위 드롭다운에서 지상파 선택
target_broadcast_btn = driver.find_element(By.CSS_SELECTOR, 'ul.list_item > li.item._item[data-text="지상파"] > a')
target_broadcast_btn.click()
time.sleep(2)

# 드라마 목록을 추출하는 함수
def extract_drama_info():
    boxes = driver.find_elements(By.CSS_SELECTOR, 'li.info_box._info_box_57')
    names = []
    ratings = []
    for box in boxes:
        try:
            name = box.find_element(By.CSS_SELECTOR, 'strong > a').text
            rating = box.find_element(By.CSS_SELECTOR, 'div.sub_info > span > span > em').text
            names.append(name)
            ratings.append(rating)
        except Exception as e:
            print(f"Error extracting drama info: {e}")
    return names, ratings

# 다음 페이지로 넘기기 함수
def go_to_next_page():
    try:
        next_page_btn = driver.find_element(By.CSS_SELECTOR, 'div.pgs > a.pg_next')
        if "disabled" in next_page_btn.get_attribute("class"):  # 버튼이 비활성화되었으면 종료
            return False
        next_page_btn.click()  # 다음 페이지로 이동
        time.sleep(2)  # 페이지 로딩 대기
        return True
    except Exception as e:
        print(f"Error going to next page: {e}")
        return False

# 드라마 목록을 계속 추출
while True:
    names, ratings = extract_drama_info()

    # 드라마 정보 저장
    for i in range(min(len(names), len(ratings))):  # 최소 길이에 맞춰 반복
        name = names[i]
        rating = ratings[i]
        drama.append([name, rating])

    # "다음 페이지" 버튼 클릭을 시도
    if not go_to_next_page():
        break  # 마지막 페이지인 경우 종료

# 드라마 정보 출력
for drama_info in drama:
    print(f'Name: {drama_info[0]}, Rating: {drama_info[1]}')

# 드라마 정보를 CSV로 저장 (선택사항)
with open('drama_info.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Drama Name', 'Rating'])
    writer.writerows(drama)

driver.quit()
