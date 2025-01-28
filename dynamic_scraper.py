from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Geckodriver yolunu belirtin
gecko_driver_path = '/usr/local/bin/geckodriver'  # Geckodriver yolunu buraya yazın

# Geckodriver servisini başlat
service = Service(gecko_driver_path)
driver = webdriver.Firefox(service=service)

# Hedef web sayfasına git
driver.get('https://www.zara.com/tr/tr/yumusak-dokulu-oversize-kaban-p03046037.html?v1=434384588&v2=2419033')

# Sayfadaki başlığı çek
title = driver.find_element(By.CSS_SELECTOR, 'h1').text
reference_number = driver.find_element(By.CSS_SELECTOR, 'button.product-color-extended-name__copy-action').text
price = driver.find_element(By.CSS_SELECTOR, 'span.money-amount__main').text
images = driver.find_elements(By.CSS_SELECTOR, 'img.product-image__image')

print(title)
print(reference_number)
price(price)

# Tarayıcıyı kapat
driver.quit()