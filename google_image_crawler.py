from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import urllib.request

query = input("검색어 입력 : ")

driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
elem = driver.find_element_by_name("q")
elem.send_keys(query)
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1.5
IMAGE_LOAD_TIME = 1.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로딩 대기
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except:
            break 
    last_height = new_height

try:
    os.mkdir(f'{query}')
except:
    pass
os.chdir(f'{query}')

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
cnt = 1
for image in images:
    try:
        image.click()
        time.sleep(IMAGE_LOAD_TIME)
        imgUrl = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img").get_attribute("src")
        urllib.request.urlretrieve(imgUrl, f'Google_{query}_{cnt:04d}.jpg')
        cnt += 1
    except:
        pass

driver.close()
