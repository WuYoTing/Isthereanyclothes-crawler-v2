import platform

from datetime import date
from crawler.prod_main import prod_main
from telegram_bot.sent_tg_msg import sent_tg_msg

os_name = platform.system()
print('os system : ' + os_name)
today_date = str(date.today())

sent_tg_msg('*' + today_date + '* *爬蟲開始* \nOs System : ' + os_name)
prod_main()
