from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import csv


driver = webdriver.Chrome()
URL = 'https://www.nielsenkorea.co.kr/tv_terrestrial_day.asp?menu=Tit_1&sub_menu=1_1&area=01'
driver.get(URL)
mylist= []
for i in range(2):
    tds = driver.find_elements(By.CSS_SELECTOR, 'table.ranking_tb >tbody>tr>td.tb_txt_center')
    td_texts = [td.text for td in tds]
td_pairs = [td_texts[i:i+2] for i in range(0, len(td_texts), 2)]
print(td_pairs)