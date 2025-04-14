from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()
URL = 'http://www.cgv.co.kr/movies/?lt=1&ft=1'
driver.get(URL)


movie = []

for i in range(5):
    rank = driver.find_elements(By.CSS_SELECTOR,'div.box-image>strong.rank')
    rank = rank[i].text
    info = driver.find_elements(By.CSS_SELECTOR, 'div.box-contents > a')
    info[i].click()
    time.sleep(2)
    title = driver.find_element(By.CSS_SELECTOR,'div.title > strong').text
    comment = driver.find_element(By.CSS_SELECTOR, '#movie_point_list_container > li:nth-of-type(1) > div.box-comment > p').text
    movie.append([rank, title,comment])
    driver.back()
    time.sleep(2)

print(movie)

local_file_path = '/home/ubuntu/damf2/data/movie/'

def save_to_csv(movie):
    with open(local_file_path +'movie_5.csv','w',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(movie)
save_to_csv(movie)