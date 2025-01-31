#Sude OZDEMIR

# Help fonksiyonu ile methodların kullanımını öğren
# help(driver.find_element)

#dir() fonksiyonu ile class'ın içinde ne var ne yok öğren
#print(dir(webdriver.Firefox))

#__doc__() ile fonksiyon veya sınıfın dökümanstasyonunu oku
#print(webdriver.Firefox.find_elements.__doc__)

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time
import os
import requests

# Geckodriver yolunu belirtin
gecko_driver_path = '/usr/local/bin/geckodriver'  # Geckodriver yolunu buraya yazın

# Geckodriver servisini başlat
service = Service(gecko_driver_path)
driver = webdriver.Firefox(service=service)

# Hedef web sayfasına git
driver.get('https://www.zara.com/tr/tr/z1975-straight-leg-high-waist-jean-p06164059.html?v1=437181794&v2=2419185')

time.sleep(2)

# Sayfadaki başlığı çek
title = driver.find_element(By.CSS_SELECTOR, 'h1').text
reference_number = driver.find_element(By.CSS_SELECTOR, 'button.product-color-extended-name__copy-action').text
price = driver.find_element(By.CSS_SELECTOR, 'span.money-amount__main').text

# CSS ile görüntüyü bul
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.media__wrapper img.media-image__image")
if image_elements:
    for product_images in image_elements:
        image_url = product_images.get_attribute("src")
        image_data = requests.get(image_url).content
        file_path_for_images = "/Users/sudeozdemir/Desktop/inditex_bot/images"
        image_name = os.path.splitext(os.path.basename(image_url))[0] + ".jpeg"
        save_path = os.path.join(file_path_for_images, image_name)
        with open (save_path, "wb") as image_file:
            image_file.write(image_data)
        print("Görsel kaydedildi.")
else:
    print("Görsel bulunamadı.")

# Tarayıcıyı kapat
driver.quit()