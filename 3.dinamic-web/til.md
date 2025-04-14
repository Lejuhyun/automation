# 2025-04-01 멜론 데이터 수집
- cd damf2/automation/ : automation 폴더로 이동하기
- 1. 크롬브라우저, 크롬 드라이버 다운로드 받기=> 리눅스환경에서 돌아가는 프로그램을 설치해야한다

1. 리눅스에서 크롬 브라우저 다운받기
- 새로운 터미널 ~ 위치에서 다운받기
```shell
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```
```shell
sudo apt --fix-broken install -y
sudo dpkg -i google-chrome-stable_current_amd64.deb
```
- 리눅스에서 크롬 드라이버 다운받기
```shell
wget https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.84/linux64/chromedriver-linux64.zip
```
- 크롬드라이버 압축 풀기
```shell
unzip chromedriver-linux64.zip 
```

2. 셀레니움을 이용할거임(파이썬버전으로 다운로드 받기)
```shell
source venv/bin/activate #활성화하기
pip install selenium
```

- 0.melon.py에 적기
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://google.com')
```

3. 멜론 데이터 가져오기 (0.melon.py)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

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

print(song_list)
```
# 4. 경로 생성해서 저장
- melon-top-100.csv라는 파일을 생성해서, song_list에 담긴 멜론 TOP 100 데이터를 CSV 형식으로 저장
```python
import csv
local_file_path = '/home/ubuntu/damf2/data/melon/'#damf폴더 => data폴더 => melon 이라는 폴더에 저장하는 경로

def save_to_csv(song_list): #song_list를 받아서 csv로 저장하는 함수
    
    with open(local_file_path + 'melon-top-100.csv', 'w', encoding='utf-8') as file: #melon-top-100이라는 파일을 생성하고 쓰기 모드로 연다
        # utf-8: 한글 깨짐 방지
        # with open: 파일을 열고 자동으로 닫아준다
        writer = csv.writer(file) # file에 데이터를 csv형식으로 쓰게 해주는 writer 객체 생성
        writer.writerows(song_list) # 여러줄을 동시에 csv 형식으로 써준다

save_to_csv(song_list) # 함수 실행한다
```
# 5. CSS 공부
## 5-1. 똑같은 태그가 여러개 있을때 원하는 태그 가져오기
- nth-of-type(숫자)
    - li:nth-of-type(1): 여러개의 li중 1번째 li태그를 가져온다!
- p:not(.foo)
    - foo 클래스가 아닌 p 태그 가져오기: 특정 클래스가 아닌 태그 가져오기
- div > *
    - div라는 클래스의 자식태그를 모두 가져오기
- span[속성이름]
    - 여러개의 태그 중 특정 속성을 갖는 태그만 가져오기
- p ~span (~: 형제 선택자)
    - p 태그 뒤에 나오는 span 태그만 가져오기
- :enabled
    - disabled가 없는 애들만 고르는 선택자
- '#'아이디이름: 특정 아이디만 가져오기
- a + span (인접형제 선택자)
    - a 태그 바루 뒤에 있는 span 태그만 가져오기
- div#foo > div.foo
- div > div > span ~code:not(.foo) : div 태그 안에 div 태그 안에 span태그의 형제선택자인 span 태그만 가져오는데 그중에서 foo를 class로 갖는애는 제외
- #id_name: #는 고유한 아이디를 불러올때 
- .class_name