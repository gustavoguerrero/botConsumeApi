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

        yesterday = datetime.today() - timedelta(days=3)
        yesterday = yesterday.strftime('%Y-%m-%d %H:%M:%S')
        yesterday = datetime.strptime(yesterday, '%Y-%m-%d %H:%M:%S')

        try:
            dateList = item.find_all("div", class_="date")[0].text.split("|")[0].strip().split()
            time = item.find_all("div", class_="date")[0].text.split("|")[1].strip()
            date = f'{dateList[0]} {dateList[2]} {dateList[4]}'
            
            monthNumber = Utils.monthTranslate(dateList[2].lower())

            fecha = f'{dateList[4]}-{monthNumber}-{dateList[0]} {time}'
            
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M')
            
            if (fecha >= yesterday and fecha <=now):

                title = item.a.text.strip()
                link = centralURL + item.find_all("a", class_='px-readon')[0]["href"]
                excerpt = item.find_all("div", class_="catItemIntroText")[0].text.strip()
                print(link)
                sendMessage(f'Publicado por @affur_bot\nTomado de la web del PIT-CNT\n\n{link}')
                

            else:
                viejo = True
                print(viejo)

        except IndexError:
            pass
        
    
    if viejo:
        requests.post(url, data = {
            'chat_id': id_admin,
            'text' : f'{now}\n\ncentral No Actualizada'
        })

def sendMessage(message):
    print(id_admin)
    
    requests.post(url, data = {
        'chat_id': id_admin, #id_channel,
        'text' : message
    })

parsearURL(centralURL)

