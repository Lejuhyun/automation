from selenium import webdriver
from selenium.webdriver.common.by import By
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
target_year_btn = driver.find_element(By.CSS_SELECTOR, 'ul.list_item > li.item._item[data-value="2020"] > a')
target_year_btn.click()
time.sleep(2)

# 지상파
broadcast_btn = driver.find_element(By.CSS_SELECTOR, 'li[data-key="broadcast"]')
target_btn_2 = broadcast_btn.find_element(By.CSS_SELECTOR, 'a')
target_btn_2.click()

# 하위 드롭다운에서 지상파 선택
target_broadcast_btn = driver.find_element(By.CSS_SELECTOR, 'ul.list_item > li.item._item[data-text="종합편성"] > a')
target_broadcast_btn.click()
time.sleep(2)

# 페이지 로딩 후, 드라마 목록을 추출
while True:
    # WebDriverWait을 사용해 요소가 로드될 때까지 기다림
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.info_box._info_box_57'))
        )
        
        boxes = driver.find_elements(By.CSS_SELECTOR, 'li.info_box._info_box_57')
        names = []
        ratings = []
        
        for box in boxes:
            # WebDriverWait을 사용해 각 드라마 이름과 시청률이 로드될 때까지 기다림
            try:
                name = box.find_element(By.CSS_SELECTOR, 'strong > a').text
                rating = box.find_element(By.CSS_SELECTOR, 'div.sub_info > span.info_txt > span.num_txt > em').text
                names.append(name)
                ratings.append(rating)
            except:
                continue  # 예외가 발생하면 이 항목은 건너뜀
        
        # 드라마 정보 저장
        for i in range(min(len(names), len(ratings))):  # 최소 길이에 맞춰 반복
            name = names[i]
            rating = ratings[i]
            drama.append([name, rating])

        # "다음 페이지" 버튼 클릭을 시도
        try:
            next_page_btn = driver.find_element(By.CSS_SELECTOR, 'div.pgs > a.pg_next')
            if "disabled" in next_page_btn.get_attribute("class"):  # 버튼이 비활성화되었으면 종료
                break
            next_page_btn.click()  # 다음 페이지로 이동
            time.sleep(2)  # 페이지 로딩 대기
        except:
            break  # 예외가 발생하면 마지막 페이지로 간 것으로 판단하고 종료
    except Exception as e:
        print(f"페이지 로딩 중 오류 발생: {e}")
        break

# 드라마 정보 출력
print(drama)

# 종료
driver.quit()