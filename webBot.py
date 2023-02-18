from datetime import date, datetime, timedelta
import requests
import json
from cfg import *

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
api = requests.get(
    'http://affur.org.uy/wp-json/wp/v2/posts'
    )

jsonDatas = json.loads(api.content)
jsonDatas = jsonDatas

def procesarMensaje():
    
    for jsonData in jsonDatas:
        viejo = False

        fecha = jsonData['date_gmt'].replace("T", " ")
        fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        

        modified = jsonData['modified_gmt'].replace("T", " ")
        modified = datetime.strptime(modified, '%Y-%m-%d %H:%M:%S')
        

        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

        yesterday = datetime.today() - timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d %H:%M:%S')
        yesterday = datetime.strptime(yesterday, '%Y-%m-%d %H:%M:%S')

        if(fecha >= yesterday and fecha <= now):
            title = jsonData['title']['rendered']
            excerpt = jsonData['excerpt']['rendered']
            excerpt = excerpt.split('>')[1].split('&')[0]
            excerpt = f'{excerpt}...'
            link = jsonData['link']

            return f'Publicado por @affur_bot\n\n{title}\n\n{excerpt}\n\nLeer más: {link}'
        else:
            viejo = True
        
    if viejo:
        requests.post(url, data = {
            'chat_id': id_admin,
            'text' : f'{now}\n\nWeb No Actualizada'
        })


def sendMessage(message):
    
    requests.post(url, data = {
        'chat_id': id_channel,
        'text' : message
    })

message = procesarMensaje()
sendMessage(message)
