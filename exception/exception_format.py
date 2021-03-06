import sys
import traceback
from telegram_bot.sent_tg_msg import sent_tg_msg
import os
from dotenv import load_dotenv


def exception_format(exception, prod_url):
    # local env
    load_dotenv()
    tg_bot = os.getenv('TG_BOT')
    tg_to = os.getenv('TG_TO')
    # sent exception tg msg
    print("Exception has been thrown. " + str(exception) + "when deal with " + prod_url)
    error_class = exception.__class__.__name__  # 取得錯誤類型
    detail = exception.args[0]  # 取得詳細內容
    cl, exc, tb = sys.exc_info()  # 取得Call Stack
    last_call_stack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    file_name = last_call_stack[0]  # 取得發生的檔案名稱
    line_num = last_call_stack[1]  # 取得發生的行號
    fun_name = last_call_stack[2]  # 取得發生的函數名稱
    error_msg = "File : \"{}\" ,\n" \
                "Line : {} ,\n" \
                "Function Name : {} ,\n" \
                "Type : [{}] ,\n" \
                "Type Detail : {} ,\n".format(file_name, line_num, fun_name, error_class, detail)
    sent_tg_msg('*Crawler Exception* \n' + error_msg + ' \nException Url : ' + prod_url)
