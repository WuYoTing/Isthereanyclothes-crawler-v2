import time
from get_selenium_page import create_driver_instance
from crawler.prod_gu import get_gu_prod
from crawler.prod_uniqlo import get_uniqlo_prod
from telegram_bot.sent_tg_msg import sent_tg_msg
from datetime import date


def prod_main():
    today_date = str(date.today())
    driver = create_driver_instance()
    # Gu
    gu_start_time = time.time()
    get_gu_prod(driver)
    gu_end_time = time.time()
    gu_total_time = gu_end_time - gu_start_time
    # Uniqlo
    uniqlo_start_time = time.time()
    get_uniqlo_prod(driver)
    uniqlo_end_time = time.time()
    uniqlo_total_time = uniqlo_end_time - uniqlo_start_time
    driver.close()
    # gu total time
    gu_prod_time = round(gu_total_time, 2)
    m, s = divmod(gu_prod_time, 60)
    h, m = divmod(m, 60)
    gu_prod_info_total = "%02d:%02d:%02d" % (h, m, s)
    # uniqlo total time
    uniqlo_prod_time = round(uniqlo_total_time, 2)
    m, s = divmod(uniqlo_prod_time, 60)
    h, m = divmod(m, 60)
    uniqlo_prod_info_total = "%02d:%02d:%02d" % (h, m, s)
    # email msg
    mail_msg = 'Gu 爬蟲使用時間 : ' + gu_prod_info_total + ' 秒\n' \
               + 'Uniqlo 爬蟲使用時間 : ' + str(uniqlo_prod_info_total) + ' 秒\n'
    sent_tg_msg('*' + today_date + '* *爬蟲完畢* \n' + mail_msg)
