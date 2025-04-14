from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome()
URL = 'https://www.oliveyoung.co.kr/store/main/getBestList.do?dispCatNo=900000100100001&fltDispCatNo=10000010002&pageIdx=1&rowsPerPage=8&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EB%A9%94%EC%9D%B4%ED%81%AC%EC%97%85'
driver.get(URL)

#for i in range(3):
    #rank = driver.find_elements(By.CSS_SELECTOR, 'span.thumb_flag.best').txt
    #print(rank)

rank = driver.find_elements(By.CSS_SELECTOR, 'span.thumb_flag.best')
brand = driver.find_elements(By.CSS_SELECTOR, 'span.tx_brand')
name = driver.find_elements(By.CSS_SELECTOR, 'p.tx_name')
mylist = []
for i in range(3):
    myrank = rank[i].text
    mybrand = brand[i].text
    myname = name[i].text
    mylist.append([myrank, mybrand, myname])
print(mylist)

local_file_path = '/home/ubuntu/damf2/data/olive/'

def save_to_csv(mylist):
    with open(local_file_path + 'oliveyoung.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(mylist)

save_to_csv(mylist)