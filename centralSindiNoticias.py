from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import requests
from utils import Utils
from cfg import *


url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

def parsearURL(urls):

    page = requests.get(urls)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div", class_="catItemView")

    for item in items:
        viejo = False
        
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

        yesterday = datetime.today() - timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d %H:%M:%S')
        yesterday = datetime.strptime(yesterday, '%Y-%m-%d %H:%M:%S')

        try:
            date = item.find_all("span", class_="catItemDateModified")[0].text.split(",")[1].strip()
        except IndexError:
            pass
        month = date.split()[1].lower()
        monthNumber = Utils.monthTranslate(month)

        fecha = f'{date.split()[2]}-{monthNumber}-{date.split()[0]} {date.split()[3]}'
         
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M')
        except ValueError:
            pass

        if(type(fecha) == datetime and fecha >= yesterday and fecha <=now):

            title = item.a.text.strip()
            link = centralURL + item.find_all("a")[0]["href"]
            excerpt = item.find_all("div", class_="catItemIntroText")[0].text.strip()
             
            sendMessage(f'Publicado por @affur_bot\nTomado de la web del PIT-CNT\n\n{link}')
            time.sleep(15)
        else:
            viejo = True
    
    if viejo:
        requests.post(url, data = {
            'chat_id': id_admin,
            'text' : f'{now}\n\nSind No Actualizada'
        })

def sendMessage(message):
    
    requests.post(url, data = {
        'chat_id': id_channel,
        'text' : message
    })

parsearURL(urls)

