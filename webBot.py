import datetime
import requests
import json
from cfg import TOKEN

api = requests.get(
    'http://affur.org.uy/wp-json/wp/v2/posts'
    )

jsonDatas = json.loads(api.content)
jsonDatas = jsonDatas

def procesarMensaje():
    
    for jsonData in jsonDatas:
        viejo = False
        date =jsonData['date'].split("T")[0]
        modified =jsonData['modified'].split("T")[0]
        today = datetime.datetime.today()#(2022,12,23)  #.today()
        today = today.strftime("%Y-%M-%d")

        if(today < modified):
            title = jsonData['title']['rendered']
            excerpt = jsonData['excerpt']['rendered']
            excerpt = excerpt.split('>')[1].split('&')[0]
            excerpt = f'{excerpt}...'
            link = jsonData['link']

            return f'Publicado por @affur_bot\n{title}\n\n{excerpt}\n\nLeer más: {link}'
        else:
            viejo = True
        
    if viejo:
        print("\n###  no hay publicaciones actuales ###")

message = procesarMensaje()

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

requests.post(url,data= {'chat_id': '@affur_uy','text' : message})


