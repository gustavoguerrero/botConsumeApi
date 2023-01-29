import requests
from cfg import id_admin, TOKEN
import datetime

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

today = datetime.datetime.today()

requests.post(url, data = {
            'chat_id': id_admin,
            'text' : f'{today}\n\nHizo pull'
        })