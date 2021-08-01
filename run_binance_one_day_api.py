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
import configparser
pd.set_option('expand_frame_repr', False)
starttime = datetime.now()
# %%
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

result_for_all
# %%
BASE_URL = str(config['biance_api_setting']['BASE_URL'])  # cofig文件裡面的幣啊安url
# %%
# 使用99天內的比較
buy_symbol_99day_dict = {}
open_data_list = {}
high_data_list = {}
low_data_list = {}
close_data_list = {}
for result_for_all_index in range(len(result_for_all)):
    print(result_for_all[result_for_all_index][0])
    onedayklineindex_url = BASE_URL + '/api/v3/klines'+'?symbol=' + \
        result_for_all[result_for_all_index][0] + '&interval=1d&limit=100'
    resp = requests.get(onedayklineindex_url)
    data = resp.json()
    if(len(data) >= 99):
        open_list = np.zeros(len(data))
        high_list = np.zeros(len(data))
        low_list = np.zeros(len(data))
        close_list = np.zeros(len(data))
        volume_list = np.zeros(len(data))
        for data_index in range(len(data)):
            # print(data[data_index][3])
            open_list[data_index] = float(data[data_index][1])  # 存open
            high_list[data_index] = float(data[data_index][2])  # 存high
            low_list[data_index] = float(data[data_index][3])  # 存low
            close_list[data_index] = float(data[data_index][4])  # 存close
            volume_list[data_index] = float(data[data_index][5])  # 存volume
        # 將100天內的收盤價用talib套件分析5日平均線，回傳list的結果
        count_sma5_list = talib.SMA(close_list, 5)
        count_sma7_list = talib.SMA(close_list, 7)
        count_sma10_list = talib.SMA(close_list, 10)
        count_sma20_list = talib.SMA(close_list, 20)
        count_sma25_list = talib.SMA(close_list, 25)
        count_sma99_list = talib.SMA(close_list, 99)
        # 使用日平均線的list最後一個值進行比較
        if(count_sma5_list[-1] <= count_sma7_list[-1] <= count_sma10_list[-1] <= count_sma20_list[-1] <= count_sma25_list[-1] <= count_sma99_list[-1]):
            buy_symbol_99day_dict[result_for_all[result_for_all_index]
                                  [0]] = (round(talib.RSI(close_list, 6)[-1], 2))  # 使用收盤價分析rsi6並將最新一個值儲存在dict裡面

# %%
# 使用25天內的比較
buy_symbol_25day_dict = {}
open_data_list = {}
high_data_list = {}
low_data_list = {}
close_data_list = {}
for result_for_all_index in range(len(result_for_all)):
    print(result_for_all[result_for_all_index][0])
    onedayklineindex_url = BASE_URL + '/api/v3/klines'+'?symbol=' + \
        result_for_all[result_for_all_index][0] + '&interval=1d&limit=100'
    resp = requests.get(onedayklineindex_url)
    data = resp.json()
    if(len(data) >= 25):
        open_list = np.zeros(len(data))
        high_list = np.zeros(len(data))
        low_list = np.zeros(len(data))
        close_list = np.zeros(len(data))
        volume_list = np.zeros(len(data))
        for data_index in range(len(data)):
            # print(data[data_index][3])
            open_list[data_index] = float(data[data_index][1])  # 存open
            high_list[data_index] = float(data[data_index][2])  # 存high
            low_list[data_index] = float(data[data_index][3])  # 存low
            close_list[data_index] = float(data[data_index][4])  # 存close
            volume_list[data_index] = float(data[data_index][5])  # 存volume
        # 將25天內的收盤價用talib套件分析5日平均線，回傳list的結果
        count_sma5_list = talib.SMA(close_list, 5)
        count_sma7_list = talib.SMA(close_list, 7)
        count_sma10_list = talib.SMA(close_list, 10)
        count_sma20_list = talib.SMA(close_list, 20)
        count_sma25_list = talib.SMA(close_list, 25)
        # 使用日平均線的list最後一個值進行比較
        if(count_sma5_list[-1] <= count_sma7_list[-1] <= count_sma10_list[-1] <= count_sma20_list[-1] <= count_sma25_list[-1]):
            buy_symbol_25day_dict[result_for_all[result_for_all_index]
                                  [0]] = (round(talib.RSI(close_list, 6)[-1], 2))  # 使用收盤價分析rsi6並將最新一個值儲存在dict裡面

# %%
# 使用20天內的比較
buy_symbol_20day_dict = {}
open_data_list = {}
high_data_list = {}
low_data_list = {}
close_data_list = {}
for result_for_all_index in range(len(result_for_all)):
    print(result_for_all[result_for_all_index][0])
    onedayklineindex_url = BASE_URL + '/api/v3/klines'+'?symbol=' + \
        result_for_all[result_for_all_index][0] + '&interval=1d&limit=100'
    resp = requests.get(onedayklineindex_url)
    data = resp.json()
    if(len(data) >= 20):
        open_list = np.zeros(len(data))
        high_list = np.zeros(len(data))
        low_list = np.zeros(len(data))
        close_list = np.zeros(len(data))
        volume_list = np.zeros(len(data))
        for data_index in range(len(data)):
            # print(data[data_index][3])
            open_list[data_index] = float(data[data_index][1])  # 存open
            high_list[data_index] = float(data[data_index][2])  # 存high
            low_list[data_index] = float(data[data_index][3])  # 存low
            close_list[data_index] = float(data[data_index][4])  # 存close
            volume_list[data_index] = float(data[data_index][5])  # 存volume
        # 將20天內的收盤價用talib套件分析5日平均線，回傳list的結果
        count_sma5_list = talib.SMA(close_list, 5)
        count_sma7_list = talib.SMA(close_list, 7)
        count_sma10_list = talib.SMA(close_list, 10)
        count_sma20_list = talib.SMA(close_list, 20)
        # 使用日平均線的list最後一個值進行比較
        if(count_sma5_list[-1] <= count_sma7_list[-1] <= count_sma10_list[-1] <= count_sma20_list[-1]):
            buy_symbol_20day_dict[result_for_all[result_for_all_index]
                                  [0]] = (round(talib.RSI(close_list, 6)[-1], 2))  # 使用收盤價分析rsi6並將最新一個值儲存在dict裡面
# %%
# 使用10天內的比較
buy_symbol_10day_dict = {}
open_data_list = {}
high_data_list = {}
low_data_list = {}
close_data_list = {}
for result_for_all_index in range(len(result_for_all)):
    print(result_for_all[result_for_all_index][0])
    onedayklineindex_url = BASE_URL + '/api/v3/klines'+'?symbol=' + \
        result_for_all[result_for_all_index][0] + '&interval=1d&limit=100'
    resp = requests.get(onedayklineindex_url)
    data = resp.json()
    if(len(data) >= 10):
        open_list = np.zeros(len(data))
        high_list = np.zeros(len(data))
        low_list = np.zeros(len(data))
        close_list = np.zeros(len(data))
        volume_list = np.zeros(len(data))
        for data_index in range(len(data)):
            # print(data[data_index][3])
            open_list[data_index] = float(data[data_index][1])  # 存open
            high_list[data_index] = float(data[data_index][2])  # 存high
            low_list[data_index] = float(data[data_index][3])  # 存low
            close_list[data_index] = float(data[data_index][4])  # 存close
            volume_list[data_index] = float(data[data_index][5])  # 存volume
        # 將20天內的收盤價用talib套件分析5日平均線，回傳list的結果
        count_sma5_list = talib.SMA(close_list, 5)
        count_sma7_list = talib.SMA(close_list, 7)
        count_sma10_list = talib.SMA(close_list, 10)
        # 使用日平均線的list最後一個值進行比較
        if(count_sma5_list[-1] <= count_sma7_list[-1] <= count_sma10_list[-1]):
            buy_symbol_10day_dict[result_for_all[result_for_all_index]
                                  [0]] = (round(talib.RSI(close_list, 6)[-1], 2))  # 使用收盤價分析rsi6並將最新一個值儲存在dict裡面

# %%
# 將 buy_symbol_99day_dict進行排序
buy_symbol_99day_sort_dict = sorted(buy_symbol_99day_dict.items(),
                                    key=lambda d: d[1], reverse=False)
# %%
buy_symbol_99day_sort_dict

# %%
buy_symbol_25day_sort_dict = sorted(buy_symbol_25day_dict.items(),
                                    key=lambda d: d[1], reverse=False)

# %%
buy_symbol_25day_sort_dict

# %%
buy_symbol_20day_sort_dict = sorted(buy_symbol_20day_dict.items(),
                                    key=lambda d: d[1], reverse=False)

# %%
buy_symbol_20day_sort_dict

# %%
buy_symbol_10day_sort_dict = sorted(buy_symbol_10day_dict.items(),
                                    key=lambda d: d[1], reverse=False)

# %%
buy_symbol_10day_sort_dict
# %%
