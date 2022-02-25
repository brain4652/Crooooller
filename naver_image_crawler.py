from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import urllib.request

query = input("검색어 입력 : ")

driver = webdriver.Chrome()
driver.get("https://search.naver.com/search.naver?where=image&sm=tab_jum&query=")
elem = driver.find_element_by_name("query")
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
        break 
    last_height = new_height

try:
    os.mkdir(f'{query}')
except:
    pass
os.chdir(f'{query}')

images = driver.find_elements_by_css_selector("._image._listImage")
cnt = 1
for image in images:
    try:
        image.click()
        time.sleep(IMAGE_LOAD_TIME)
        imgUrl = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/section[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div/div[1]/div[1]/img").get_attribute("src")
        urllib.request.urlretrieve(imgUrl, f'Naver_{query}_{cnt:04d}.jpg')
        cnt += 1
    except:
        pass

driver.close()
