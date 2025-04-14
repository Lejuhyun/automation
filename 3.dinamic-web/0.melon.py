from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
import csv
driver = webdriver.Chrome()

URL = 'https://www.melon.com/chart/index.htm'
driver.get(URL)

song_info = driver.find_elements(By.CSS_SELECTOR, 'a.btn.song_info') # btn song_info를 포함한 줄을 가져온다
# print(song_info)

song_list = []

for i in range(3):
    song_info[i].click() # 차트에 있는 곡의 상세정보를 마우스로 누른다
    time.sleep(2) # 2초 기다리기

    title = driver.find_element(By.CSS_SELECTOR, 'div.song_name').text #'song_name'이라는 클래스를 가지는 div태그를 찾아야함
    artist = driver.find_element(By.CSS_SELECTOR,'div.artist span').text # 'artist'라는 클래스를 가진 div 태그 아래 span 태그 가져와야함
    # 여러개의 dd를 찾은 뒤 인덱스 접근하기 (meta라는 클래스 하위에 dd가 4개나 있음 => find_elements를 통해 전부 가져옴)
    # meta_data = driver.find_elements(By.CSS_SELECTOR, 'div.meta dd') 

    # 발매일 정보를 특정
    publish_date = driver.find_element(By.CSS_SELECTOR, 'dl.list > dd:nth-of-type(2)').text
    like_cnt = driver.find_element(By.CSS_SELECTOR, 'span#d_like_count').text

    # like_cnt의 쉼표를 공백으로 바꿔준다
    like_cnt = like_cnt.replace(',', '')
    song_list.append([title,artist,publish_date,like_cnt])
    driver.back() # 뒤로가기


local_file_path = '/home/ubuntu/damf2/data/melon/'#damf폴더 => data폴더 => melon 이라는 폴더에 저장하는 경로

def save_to_csv(song_list): #csv로 저장하기
    
    with open(local_file_path + 'melon-top-100.csv', 'w', encoding='utf-8') as file: #damf폴더 => data폴더 => melon => melon-top-100이라는 파일을 생성하고 file이라고 부를거임
        writer = csv.writer(file)
        writer.writerows(song_list) # 여러줄을 동시에 써주는 함수

save_to_csv(song_list)
