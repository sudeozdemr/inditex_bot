#Sude OZDEMIR

import requests, time, logging, os, sys, pandas as pd

from deep_translator import GoogleTranslator
from telegram import Update 
from telegram.ext import MessageHandler, Updater, CommandHandler, Application, filters, ContextTypes

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

#TODO iptal komutu ekle. for döngüsünde işini halledip cancel komutunu işliyor. Ben cancel komutuna bastığım anca döngü içinde bile olsa basmalı yani sys exiti döngü içine etki edebilir şekilde yaz.
#TODO farklı tarayıcılar adapte et.
#TODO firefox açılıp durmasın.
#TODO beyaz imagelerı kaldır.

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

#CommandHandler 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! I'm a telegram bot, send me a  URL!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please send me a  Web-site URL.")

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You have canceled scraping.")
    sys.exit(0)

#ErrorHandler
async def error_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"An error occurred: {context.error}")
    await update.message.reply_text("An error has occurred! Please try again later.")    

#Message Handler


#Functions
async def keyboardinfo (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #TODO Gelen mesajı fonksiyon içine almadan değişkende tut
    user_url = update.message.text
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0"}

    # Geckodriver yolunu belirtin
    gecko_driver_path = '/usr/local/bin/geckodriver'  # Geckodriver yolunu buraya yazın

    # Geckodriver servisini başlat
    service = Service(gecko_driver_path)
    driver = webdriver.Firefox(service=service) #Firefox'un açılmasını sağlayan kod bloğu

    # Hedef web sayfasına git
    driver.get(user_url)

    time.sleep(2)

    if "mobile" in user_url:
        #app_url_for_scrap = soup.find('meta', property='og:url')
        title = driver.find_element(By.CSS_SELECTOR, 'h1').text
        translator = GoogleTranslator(source='auto', target='tr')
        app_title = translator.translate(app_title)

        await update.message.reply_text(f"{app_title}")
    
    else:
        title = driver.find_element(By.CSS_SELECTOR, 'h1').text
        reference_number = driver.find_element(By.CSS_SELECTOR, 'button.product-color-extended-name__copy-action').text
        price = driver.find_element(By.CSS_SELECTOR, 'span.money-amount__main').text

        # CSS ile görüntüyü bul
        image_elements = driver.find_elements(By.CSS_SELECTOR, "div.media__wrapper img.media-image__image")
        if image_elements:
            for product_images in image_elements:
                image_url = product_images.get_attribute("src")
                image_data = requests.get(image_url).content
                
                await update.message.reply_photo(image_data)
               
        else:
            print("Görsel bulunamadı.")

        await update.message.reply_text(f"Title: {title} \nPrice: {price} \nReference number: {reference_number} \n")
        # Tarayıcıyı kapat
    driver.quit()
                


#Starting the bot 
if __name__ == "__main__":

    #Read the bot token
    BOT_TOKEN = open("/Users/sudeozdemir/Desktop/inditex_bot/inditex_bot_token.txt", "r").read().strip()

    #application nesnesi oluşturuldu botu çalışmatırmak istediğimizde bu nesne üzerinden işlem yapacağız.
    application = Application.builder().token(BOT_TOKEN).build()

    #Commmand_handler
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command ))
    application.add_handler(CommandHandler("cancel", cancel_command))

    #ErrorHandler 
    application.add_error_handler(error_command)

    #Message Handlerı bot üstünden çağırdığımız kod parçası
    application.add_handler(MessageHandler(filters.TEXT, keyboardinfo ))

    #botu çalıştıran kod betiği
    application.run_polling()



