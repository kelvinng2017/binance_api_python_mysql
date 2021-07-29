# %%
import pymysql

import time
import requests
from datetime import datetime
# import time
# import dataframe_image as dfi
import pandas as pd
# talib
import talib
import btalib
import numpy as np
import matplotlib.pyplot as plt
import mpl_finance as mpf
import configparser
pd.set_option('expand_frame_repr', False)
starttime = datetime.now()
# %%
config = configparser.ConfigParser()
config.read('D:\config_file\python_mysql_binance\config.ini')
config.sections()
# %%
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
# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料sql語法
        command = "SELECT  `symbol_name` FROM symbol_data_table"

        # 執行指令
        cursor.execute(command)

        # 取得所有資料
        result_for_all = cursor.fetchall()

        print("查詢全部資料成功")
        conn.close()
except Exception as ex:
    print(ex)
# %%
result_for_all

# %%
result_for_all[1][0]
# %%

while(datetime.now().minute <= 61):
    now_time_new = str(datetime.now().year)+"-"+str(datetime.now().month)+"-" + str(datetime.now().day)+" "+str(
        datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)+"."+str(datetime.now().microsecond)
    print(now_time_new)
    high_hand_dict = {}
    BASE_URL = str(config['biance_api_setting']['BASE_URL'])
    limit = str(config['biance_api_setting']['limit'])
    for symbol_index in range(len(result_for_all)):
        print(result_for_all[symbol_index][0])
        BASE_URL = str(config['biance_api_setting']['BASE_URL'])

        kline = '/api/v3/trades'
        kline_url = BASE_URL + kline + '?' + 'symbol=' + \
            result_for_all[symbol_index][0]+'&limit='+limit
        resp = requests.get(kline_url)
        high_hand_dict[result_for_all[symbol_index][0]] = resp.json()[-1]['time'] - \
            resp.json()[0]['time']

    hig_hand_tuple = sorted(high_hand_dict.items(),
                            key=lambda d: d[1], reverse=False)[0:10]

    symbol_dict = {}
    new_sma_symbol = {}
    old_sma_symbol = {}
    to_rsi6_symbol = {}

    rsi = {}

    for hig_hand_tuple_index_1minute in hig_hand_tuple:
        print(hig_hand_tuple_index_1minute[1])
        onedayklineindex_url = BASE_URL + '/api/v3/klines'+'?symbol=' + \
            hig_hand_tuple_index_1minute[0] + '&interval=1m&limit=100'
        resp = requests.get(onedayklineindex_url)
        data = resp.json()
        close_numpy = np.zeros(len(data))
        opend_data = data[-1][1]  # 抓open資料
        high_data = data[-1][2]  # 抓high資料
        low_data = data[-1][3]  # 抓low資料
        close_data = data[-1][4]  # 抓close的資料
        volume_data = data[-1][5]  # 抓volume的資料
        # print(len(data))
        for data_index in range(len(data)):
            # print(data[data_index][3])
            close_numpy[data_index] = float(data[data_index][4])  # 存close

        rsi[hig_hand_tuple_index_1minute[0]] = talib.RSI(close_numpy, 6)
        to_rsi6_symbol[hig_hand_tuple_index_1minute[0]] = round(
            float(rsi[hig_hand_tuple_index_1minute[0]][-1]), 2)

    # hig_hand_tuple
    now_time = str(datetime.now().year)+"-"+str(datetime.now().month)+"-" + str(datetime.now().day)+" "+str(
        datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)+"."+str(datetime.now().microsecond)
    # now_time

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings_for_high_hand)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 建立資料表指令
            command_create_datatable = "CREATE TABLE `%s`(symbol_id INT NOT NULL AUTO_INCREMENT, symbol_name VARCHAR(100) NOT NULL ,high_hand_time VARCHAR(100) NOT NULL,rsi6 VARCHAR(10),open VARCHAR(100),high VARCHAR(100),low VARCHAR(100),close VARCHAR(100),volume VARCHAR(100),PRIMARY KEY(symbol_id))"

            # 執行指令
            cursor.execute(command_create_datatable, [now_time])

            command_insert_data = "INSERT INTO `%s`(symbol_name,high_hand_time,open,high,low,close,volume)VALUES(%s,%s,%s,%s,%s,%s,%s)"

            for hig_hand_tuple_index_1minute in hig_hand_tuple:
                print(hig_hand_tuple_index_1minute[1])
                onedayklineindex_url = BASE_URL + '/api/v3/klines'+'?symbol=' + \
                    hig_hand_tuple_index_1minute[0] + '&interval=1m&limit=100'
                resp = requests.get(onedayklineindex_url)
                data = resp.json()
                close_numpy = np.zeros(len(data))
                opend_data = data[-1][1]  # 抓open資料
                high_data = data[-1][2]  # 抓high資料
                low_data = data[-1][3]  # 抓low資料
                close_data = data[-1][4]  # 抓close的資料
                volume_data = data[-1][5]  # 抓volume的資料
                cursor.execute(command_insert_data,
                               [now_time, hig_hand_tuple_index_1minute[0], str(hig_hand_tuple_index_1minute[1]),
                                str(opend_data), str(high_data), str(low_data), str(close_data), str(volume_data)])
                # print(len(data))
                for data_index in range(len(data)):
                    # print(data[data_index][3])
                    close_numpy[data_index] = float(
                        data[data_index][4])  # 存close

                rsi[hig_hand_tuple_index_1minute[0]
                    ] = talib.RSI(close_numpy, 6)
                to_rsi6_symbol[hig_hand_tuple_index_1minute[0]] = round(
                    float(rsi[hig_hand_tuple_index_1minute[0]][-1]), 2)

            conn.commit()
            print("建立資料表成功")
            conn.close()
    except Exception as ex:
        print(ex)

    to_rsi6_symbol_sort = sorted(to_rsi6_symbol.items(),
                                 key=lambda d: d[1], reverse=False)

    # to_rsi6_symbol_sort[0][0]

    # 修改特定小幣名稱
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings_for_high_hand)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 修改資料SQL語法
            command = "UPDATE  `%s` SET rsi6 = %s WHERE symbol_name = %s"

            # 執行指令
            for to_rsi6_symbol_sort_index in range(len(to_rsi6_symbol_sort)):
                cursor.execute(command, [now_time, str(
                    to_rsi6_symbol_sort[to_rsi6_symbol_sort_index][1]), to_rsi6_symbol_sort[to_rsi6_symbol_sort_index][0]])

                # 儲存變更
                conn.commit()

            print("修改資料成功")
            conn.close()
    except Exception as ex:
        print(ex)

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings_for_high_hand_table_name)

        # 建立Cursor物件
        with conn.cursor() as cursor:

            command_insert_data = "INSERT INTO name_table(table_name)VALUES(%s)"
            cursor.execute(command_insert_data,
                           [now_time])

            conn.commit()
            print("建立資料表名稱成功")
            conn.close()
    except Exception as ex:
        print(ex)


# %%
data[-1][1]

# %%
