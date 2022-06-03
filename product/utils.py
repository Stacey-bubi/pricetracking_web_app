from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, Request
from .models import Link



url = "https://www.wildberries.ru/catalog/28777922/detail.aspx?targetUrl=RG"
#url="https://www.wildberries.ru/catalog/53395519/detail.aspx?targetUrl=GP"
#url = "https://www.wildberries.ru/catalog/72810711/detail.aspx?targetUrl=GP"
#url = "https://www.wildberries.ru/catalog/8429560/detail.aspx"
#url = "https://www.wildberries.ru/catalog/8423798/detail.aspx?targetUrl=GP"
#url = "https://www.wildberries.ru/catalog/5442259/detail.aspx?targetUrl=WR"

def get_data(url):
        ser = Service("/Users/stacey/Documents/CodeTests_Projects/drivers/chromedriver")
        op = webdriver.ChromeOptions()
        op.add_argument("headless")
        driver = webdriver.Chrome(service=ser, options=op)
        driver.get(url)
        time.sleep(4)

        main_page = driver.page_source
        
        driver.quit()
        soup = BeautifulSoup( main_page, "lxml")
        html = soup.find("h1", class_="same-part-kt__header")
        raw_name = html.find_all("span")
        name=''
        for span in raw_name:
                name = span.text + " " + name
        name = name.strip()
        raw_price = soup.find("span", class_="price-block__final-price")
        current_price = raw_price.text
        price_filter = filter(str.isdigit, current_price)
        price = int("".join(price_filter))

        return name, price
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
def data_chrome(url):
        ser = Service("/Users/stacey/Documents/CodeTests_Projects/drivers/chromedriver")
        op = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ser, options=op)
        driver.get(url)
        time.sleep(6)
        name = driver.find_element(By.CLASS_NAME, "same-part-kt__header").text
        raw_price = driver.find_element(By.CLASS_NAME, "price-block__content").text
        price = float(raw_price.partition("\n")[0].replace(" ", "")[:-1])
        driver.quit()
        return name, price


def get_link_data(url):
        headers = {"User Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

        r = Request(url, headers=headers)
        rr = urlopen(r).read()
        soup = BeautifulSoup(rr, "lxml")

        html = soup.find("h1", class_="same-part-kt__header")
        raw_name = html.find_all("span")
        name=''
        for span in raw_name:
                name = span.text + " " + name
        name = name.strip()

        raw_price = soup.find("span", class_="price-block__final-price")
        current_price = raw_price.text
        price_filter = filter(str.isdigit, current_price)
        price = float("".join(price_filter))

        return name, price

       
def data_safari(url):
    space = "\xa0"
    browser = webdriver.safari.webdriver.WebDriver(quiet=False)
    browser.get(url)

    time.sleep(0.5)

    name = browser.find_element(By.CLASS_NAME, "same-part-kt__header").text
    raw_price = browser.find_element(By.CLASS_NAME, "price-block__final-price").text
    price = raw_price.partition("\n")[0].replace(space, "").strip()[:-1]
 
    if price == '':
            price = 0
    print(price)
    #else: price = float(price)
    
    #image = browser.find_element(By.CLASS_NAME, "slide__content img-plug j-wba-card-item")
    
    #jpg = browser.find_element(By.CSS_SELECTOR, "img.content")

    jpg = (browser.find_element(by=By.XPATH, value='//img[@alt=" Вид 1."]')).get_attribute('src')
    browser.quit()

    return name, price, jpg

#print(data_safari(url))
#data_safari(url)
#print(get_link_data(url))
#info = get_data(url)
#print(info[1])
def track_for_discount():
    items = Link.objects.all()  #take a list of existed items
    print(items)
    for item in items:
        data = get_data(item.url)
        if data[1] < item.current_price:
            item_discount = Link.objects.get(id=item.id)  #take particular object
            item_discount.old_price = item_discount.current_price
            item_discount.current_price = data[1]
            item_discount.save(update_fields=['current_price, old_price'])
#track_for_discount()