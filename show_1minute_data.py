
import pandas as pd
import pymysql
from datetime import datetime
import time
import configparser
config = configparser.ConfigParser()
config.read('D:\config_file\python_mysql_binance\config.ini')
config.sections()

# 資料庫設定
db_settings = {
    "host": config['database_settings']['host'],
    "port": int(config['database_settings']['port']),
    "user": config['database_settings']['user'],
    "password": config['database_settings']['password'],
    "db": config['database_settings']['db'],
    "charset": config['database_settings']['charset']
}
db_settings_for_high_hand = {
    "host": config['database_settings']['host'],
    "port": int(config['database_settings']['port']),
    "user": config['database_settings']['user'],
    "password": config['database_settings']['password'],
    "db": config['database_settings']['db_high_hand'],
    "charset": config['database_settings']['charset']
}
db_settings_for_high_hand_table_name = {
    "host": config['database_settings']['host'],
    "port": int(config['database_settings']['port']),
    "user": config['database_settings']['user'],
    "password": config['database_settings']['password'],
    "db": config['database_settings']['db_high_hand_table_name'],
    "charset": config['database_settings']['charset']
}
while(datetime.now().minute <= 61):
    try:
        # 建立Connection物件
        # 讀取tabel_name資料庫的name_table資料表的table_name欄位
        conn = pymysql.connect(**db_settings_for_high_hand_table_name)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料sql語法
            # 使用逆序排序的方式讀取最新寫入到資料庫最新資料表名稱
            command = "SELECT table_name FROM name_table ORDER BY table_name_id DESC LIMIT 0,1;"

            # 執行指令
            cursor.execute(command)

            # 取得所有資料
            result_for_all = cursor.fetchall()

            print("查詢最新資料表名稱成功")
            conn.close()
    except Exception as ex:
        print(ex)

    # result_for_all[0][0]

    try:
        # 建立Connection物件
        # 讀取tabel_name資料庫的name_table資料表的table_name欄位
        conn = pymysql.connect(**db_settings_for_high_hand)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料sql語法
            # 使用逆序排序的方式讀取最新寫入到資料庫最新資料表名稱
            command = "SELECT symbol_name,high_hand_time,rsi6,open,high,low,close,volume FROM `%s`;"

            # 執行指令
            cursor.execute(command, [result_for_all[0][0]])

            # 取得所有資料
            result_data_1minute = cursor.fetchall()
            df = pd.DataFrame(list(result_data_1minute), columns=[
                'symbol_name', 'high_hand_time', 'rsi6', 'open', 'high', 'low', 'close', 'volume'])

            print("查詢全部1分鍾資料成功")
            conn.close()
    except Exception as ex:
        print(ex)
    print(result_for_all[0][0])
    print(df)
    time.sleep(10)  # 10秒更新一次
