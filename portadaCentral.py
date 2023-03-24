from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import requests
from utils import Utils
from cfg import *



url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

def parsearURL(urlp):

    page = requests.get(urlp)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div", class_="sprocket-features-padding")
    
    for item in items:
        viejo = False   
        
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

        yesterday = datetime.today() - timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d %H:%M:%S')
        yesterday = datetime.strptime(yesterday, '%Y-%m-%d %H:%M:%S')

        try:
            dateList = item.find_all("div", class_="date")[0].text.split("-")[0]
            time = item.find_all("div", class_="date")[0].text.split("|")[1]
            print(dateList)
            date = f'{dateList[0]} {dateList[1]} {dateList[2]}'
            print(date)
            monthNumber = Utils.monthTranslate(dateList[1].lower())

            fecha = f'{dateList[4]}-{monthNumber}-{dateList[0]} {time}'
            print(fecha)
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M')
            if (fecha >= yesterday and fecha <=now):

                title = item.a.text.strip()
                link = centralURL + item.find_all("a")[0]["href"]
                excerpt = item.find_all("div", class_="catItemIntroText")[0].text.strip()
                
                sendMessage(f'Publicado por @affur_bot\nTomado de la web del PIT-CNT\n\n{link}')
                time.sleep(15)
            else:
                viejo = True
            
        except IndexError:
            pass
        
    
    if viejo:
        requests.post(url, data = {
            'chat_id': id_admin,
            'text' : f'{now}\n\ncentral No Actualizada'
        })
def sendMessage(message):
    
    requests.post(url, data = {
        'chat_id': id_admin, #id_channel,
        'text' : message
    })

parsearURL(centralURL)

