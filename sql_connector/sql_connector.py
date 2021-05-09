import pymysql
import os
from dotenv import load_dotenv
from datetime import date
import time


def sql_connector(prod_sex, prod_category, prod_name, prod_price, prod_number, prod_about,
                  prod_material, prod_url, prod_main_image_url, prod_size_url, prod_is_new_good,
                  prod_is_online_only, prod_is_set, prod_is_limited_time, prod_is_price_down,
                  prod_can_modify, prod_limited_price_date, prod_get_time, table_name):
    # load db
    load_dotenv()
    db_host = os.getenv('Crawler_DB_IP')
    db_name = os.getenv('Crawler_DB_Name')
    db_user_name = os.getenv('Crawler_DB_User')
    db_password = os.getenv('Crawler_DB_Password')
    # start db connection
    connection = pymysql.connect(
        host=db_host,
        database=db_name,
        user=db_user_name,
        password=db_password
    )
    try:
        if connection.open:
            cursor = connection.cursor()
            # check if had record
            check_prod_record_sql = "SELECT * FROM " + table_name + " WHERE prod_number = '" + \
                                    prod_number + "'"
            cursor.execute(check_prod_record_sql)
            results = cursor.fetchall()
            row_count = cursor.rowcount
            # if no record add data
            if row_count == 0:
                print("沒有 " + prod_name + " 的紀錄,新增一筆")
                add_clothe_data = "INSERT INTO " + table_name + \
                                  " (sex, category, name, prod_number, about, material" \
                                  ", url,main_image_url, size_url, is_new_good, is_online_only" \
                                  ", is_set, is_limited_time,is_price_down, can_modify" \
                                  ", limited_price_date,recording_date,current_price) " \
                                  "VALUES (%s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s" \
                                  ", %s,%s, %s, %s, %s);"
                clothes_data = (
                    prod_sex, prod_category, prod_name, prod_number, prod_about, prod_material,
                    prod_url, prod_main_image_url, prod_size_url, prod_is_new_good,
                    prod_is_online_only, prod_is_set, prod_is_limited_time, prod_is_price_down,
                    prod_can_modify, prod_limited_price_date, prod_get_time, prod_price
                )
                cursor.execute(add_clothe_data, clothes_data)
            # if had record update data
            else:
                print("已有 " + prod_name + " 的紀錄,更新資料")
                update_clothe_data = "UPDATE " + table_name + \
                                     " SET sex = %s,category= %s,name= %s,about= %s,material= %s" \
                                     ",url= %s,main_image_url= %s,size_url= %s,is_new_good= %s" \
                                     ",is_online_only= %s,is_set= %s,is_limited_time= %s" \
                                     ",is_price_down= %s,can_modify= %s,limited_price_date= %s" \
                                     ",recording_date= %s,current_price= %s WHERE prod_number= %s "
                clothes_data = (
                    prod_sex, prod_category, prod_name, prod_about, prod_material, prod_url,
                    prod_main_image_url, prod_size_url, prod_is_new_good, prod_is_online_only,
                    prod_is_set, prod_is_limited_time, prod_is_price_down, prod_can_modify,
                    prod_limited_price_date, prod_get_time, prod_price, prod_number
                )
                cursor.execute(update_clothe_data, clothes_data)

        # check if today data exist
        check_log_record_sql = "SELECT * FROM " + table_name + \
                               "_price_log WHERE prod_number = '" + prod_number + \
                               "' AND DATE(recording_date)" + " LIKE '" \
                               + time.strftime('%Y-%m-%d') + "%'"
        cursor.execute(check_log_record_sql)
        results = cursor.fetchall()
        row_count = cursor.rowcount
        # if no record
        if row_count == 0:
            # add price log
            insert_log_sql = "INSERT INTO " + table_name + "_price_log (prod_number, price," \
                                                           "recording_date) VALUES (%s, %s, %s);"
            new_data = (prod_number, prod_price, prod_get_time)
            cursor.execute(insert_log_sql, new_data)
            connection.commit()
        else:
            print("今天已有 " + prod_name + " 的紀錄,跳過")
    except pymysql.Error as Ec:
        print("資料庫連接失敗：", Ec)
    finally:
        if connection.open:
            cursor.close()
            connection.close()
