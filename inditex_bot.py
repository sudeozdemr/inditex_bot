import requests

from bs4 import BeautifulSoup
from telegram import Update 
from telegram.ext import MessageHandler, Updater, CommandHandler, Application, filters, ContextTypes


#Fonksions
async def keyboardinfo (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #TODO Gelen mesajı fonksiyon içine almadan değişkende tut
    user_url = update.message.text 

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0"}

    #Siteye istek at
    response = requests.get(user_url, headers=headers)
    response.raise_for_status()

    #HTML içeriğini ayrıştır
    soup = BeautifulSoup(response.content, 'html.parser')

    if "zara.com/tr" in user_url:
        titles = soup.find("h1", class_ ="product-detail-info__header-name" ).get_text()
        price = soup.find("span", class_ = "money-amount__main").get_text()
        reference_number = soup.find("button", class_="product-color-extended-name__copy-action").get_text()
    else :
        titles = soup.find("h1", class_ ="product-detail-info__header-name")
        price = soup.find("span", class_ = "money-amount__main")
        reference_number = soup.find("button", class_="product-color-extended-name__copy-action")

    await update.message.reply_text(f"Title: {titles} \nPrice: {price} \nReference number: {reference_number}")


#CommandHandler 

#MessageHandler


#Starting the bot 
if __name__ == "__main__":

    #Read the bot token
    BOT_TOKEN = open("/Users/sudeozdemir/Desktop/inditex_bot/inditex_bot_token.txt", "r").read().strip()

    #application nesnesi oluşturuldu botu çalışmatırmak istediğimizde bu nesne üzerinden işlem yapacağız.
    application = Application.builder().token(BOT_TOKEN).build()

    #Message Handlerı bot üstünden çağırdığımız kod parçası
    application.add_handler(MessageHandler(filters.TEXT, keyboardinfo ))

    #botu çalıştıran kod betiği
    application.run_polling()



