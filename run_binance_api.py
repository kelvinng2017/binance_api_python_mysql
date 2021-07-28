# %%
import pymysql
import datetime
import time
import requests

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
starttime = datetime.datetime.now()
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

# %%
hig_hand_tuple = sorted(high_hand_dict.items(),
                        key=lambda d: d[1], reverse=False)[0:10]

# %%
hig_hand_tuple[1][1]
# %%
now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
# %%
now_time
# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings_for_high_hand)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 建立資料表指令
        command_create_datatable = "CREATE TABLE " + now_time + \
            "(symbol_id INT NOT NULL AUTO_INCREMENT, symbol_name VARCHAR(100) NOT NULL ,high_hand_time VARCHAR(100) NOT NULL ,PRIMARY KEY(symbol_id));"

        # 執行指令
        cursor.execute(command_create_datatable)

        command_insert_data = "INSERT INTO " + \
            now_time + "(symbol_name,high_hand_time)VALUES(%s,%s)"

        for hig_hand_tuple_index in range(len(hig_hand_tuple)):
            print(hig_hand_tuple[hig_hand_tuple_index][0] +
                  ","+hig_hand_tuple[hig_hand_tuple_index][1])
            cursor.execute(command_create_datatable,
                           (hig_hand_tuple[hig_hand_tuple_index][0], hig_hand_tuple[hig_hand_tuple_index][1]))

        print("建立資料表成功")
        conn.close()
except Exception as ex:
    print(ex)
# %%
# %%
symbol_dict = {}
new_sma_symbol = {}
old_sma_symbol = {}
to_rsi6_symbol = {}

# %%
rsi = {}
for hig_hand_tuple_index_1minute in hig_hand_tuple:
    # print(hig_hand_tuple_index_1minute[0])
    onedayklineindex_url = BASE_URL + '/api/v3/klines'+'?symbol=' + \
        hig_hand_tuple_index_1minute[0] + '&interval=1m&limit=100'
    resp = requests.get(onedayklineindex_url)
    data = resp.json()
    close_numpy = np.zeros(len(data))
    # print(len(data))
    for data_index in range(len(data)):
        # print(data[data_index][3])
        close_numpy[data_index] = float(data[data_index][4])  # 存close

    rsi[hig_hand_tuple_index_1minute[0]] = talib.RSI(close_numpy, 6)
    to_rsi6_symbol[hig_hand_tuple_index_1minute[0]] = round(
        float(rsi[hig_hand_tuple_index_1minute[0]][-1]), 2)

# %%
to_rsi6_symbol_sort = sorted(to_rsi6_symbol.items(),
                             key=lambda d: d[1], reverse=False)

# %%
to_rsi6_symbol_sort
