import datetime
import requests
import json
from cfg import TOKEN, id_admin

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
api = requests.get(
    'http://resoluciones.affur.org.uy/wp-json/wp/v2/posts'
    )

jsonDatas = json.loads(api.content)
jsonDatas= jsonDatas

def procesarMensaje():
    
    for jsonData in jsonDatas:
        date =jsonData['date'].split("T")[0]
        modified =jsonData['modified'].split("T")[0]
        today = datetime.datetime.today()
        today = today.strftime("%Y-%M-%d")

        if(today < modified):
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
            'text' : f'{today}\n\nWeb No Actualizada'
        })


def sendMessage(message):
    
    requests.post(url,data = {
        'chat_id': '@affur_uy',
        'text' : message
    })

message = procesarMensaje()
sendMessage(message)