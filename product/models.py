from django.db import models
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from django.core.validators import validate_image_file_extension
from sqlalchemy import null

def data_safari(url):
    space = "\xa0"
    browser = webdriver.safari.webdriver.WebDriver(quiet=False)
    browser.get(url)

    time.sleep(2)

    name = browser.find_element(By.CLASS_NAME, "same-part-kt__header").text
    raw_price = browser.find_element(By.CLASS_NAME, "price-block__final-price").text
    price = float(raw_price.partition("\n")[0].replace(space, "").strip()[:-1])
    image = (browser.find_element_by_xpath('//img[@alt=" Вид 1."]')).get_attribute("src")
    if price == '':
            price = 0
    else: price = float(price)
    browser.quit()

    return name, price, image

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
        price = float("".join(price_filter))

        return name, price

class Link(models.Model):
    name = models.CharField(max_length=200, blank=True)
    url = models.URLField()
    current_price = models.FloatField(blank=True, null=True)
    old_price = models.FloatField(blank=True)
    price_difference = models.FloatField(blank=True)
    date_created = models.DateField(auto_created=True,blank=True, null=True)
    date_updated = models.DateField(auto_now_add=True, blank=True, null=True)
    monitored = models.BooleanField(default=False, blank=True, null=True)
    image = models.FileField('photo', upload_to="product-thumbnails", validators=[validate_image_file_extension], null=True)
    
    
    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['date_created']

    

    def save(self, *args, **kwargs):
        name, price, image = data_safari(self.url)
        old_price = self.current_price
        if self.current_price:
            if price != old_price:
                difference = price - old_price
                self.price_difference = round(difference, 2)
                self.old_price = old_price
                
        else:
            self.price_difference = 0
            self.old_price = 0
        self.name = name
        self.current_price = price

        self.image = image

        super().save(*args, **kwargs)
        



