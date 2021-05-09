import requests
import os
from dotenv import load_dotenv


def sent_tg_msg(text):
    # local env
    load_dotenv()
    tg_bot = os.getenv('TG_BOT')
    tg_to = os.getenv('TG_TO')
    # sent tg message
    man_index_res = requests.get(
        'https://api.telegram.org/bot' + tg_bot + '/sendMessage?chat_id=' + tg_to +
        '&parse_mode=Markdown&text=' + text
    )
    print(man_index_res.json())
