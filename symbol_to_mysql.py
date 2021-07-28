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

# %%

BASE_URL = config['biance_api_setting']['BASE_URL']
symbol_url = BASE_URL+config['biance_api_setting']['api_url']+'ticker/price'
resp_symbol = requests.get(symbol_url)
data_symbol = resp_symbol.json()
# %%
# data_symbol
# %%
data_symbol_pandas = pd.DataFrame(
    data_symbol, columns={'symbol': 'symbol', 'price': 'price'})
# %%
data_usdt_symbol_pandas = data_symbol_pandas[data_symbol_pandas.symbol.str.contains(
    "USDT")]

# %%
data_usdt_symbol_pandas
# %%
need_usdt_price_symbol_numpy = np.array(
    data_usdt_symbol_pandas['symbol'], dtype=str)
# %%
get_1m_sma = {}
need_usdt_price_symbol_numpy_out = {}
use_time_dict = {}
symbol_dict = {}
price_dict = {}
sort_use_time_dict = {}
# %%
need_usdt_price_symbol_numpy = np.array(
    data_usdt_symbol_pandas['symbol'], dtype=str)
# %%
i = 0
for need_usdt_price_symbol_numpy_out_index in range(len(need_usdt_price_symbol_numpy)):
    if (need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("DOWN") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("UP") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BIDR") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("NGN") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BUSD") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDC") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("IDRT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BVND") == -1
        and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDTRUB") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BTCSTUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BEAR") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BULL") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDTBKRW") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("EURUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDTTRY") and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("GBPUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDTDAI") == -1
        and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDTZAR") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("AUDUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BCHABCUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BKRWUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDTUAH") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("TUSDUSDT") == -1
        and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BCCUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BCCUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("HCUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDSUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("PAXUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("USDTBRL") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("BCHSVUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("STRATUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("SUSDUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("LENDUSDT") == -1
            and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("VENUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("XZCUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("STORMUSDT") == -1) and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("MCOUSDT") == -1 and need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index].find("DAIUSDT") == -1:
        need_usdt_price_symbol_numpy_out[i] = need_usdt_price_symbol_numpy[need_usdt_price_symbol_numpy_out_index]
        i = i+1
i = 0

# %%
need_usdt_price_symbol_numpy_out

# %%
need_usdt_price_symbol_numpy_out
# %%
# %%
need_usdt_price_symbol_numpy_out[len(
    need_usdt_price_symbol_numpy_out)] = "BNBUSDT"

# %%
need_usdt_price_symbol_numpy_out[len(
    need_usdt_price_symbol_numpy_out)] = "SHIBUSDT"
# %%
# 將需要的幣名稱存在mysql上
# 批量新增

try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料sql語法
        command = "INSERT INTO symbol_data_table(symbol_name)VALUES(%s)"

        # 執行指令
        for need_usdt_price_symbol_numpy_index in need_usdt_price_symbol_numpy_out.values():
            print(need_usdt_price_symbol_numpy_index)
            cursor.execute(command, (need_usdt_price_symbol_numpy_index))
        conn.commit()
        print("批量新增資料成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
# 單筆新增
"""
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料sql語法
        command = "INSERT INTO symbol_data_table(symbol_name)VALUES(%s)"

        # 執行指令

        cursor.execute(command, ("SHIBUDT"))
        conn.commit()
        print("單筆新增資料成功")
        conn.close()
except Exception as ex:
    print(ex)
"""
# %%
# 查詢全部小幣的名稱
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
result_for_all[0][0]

# %%
# 查詢第一筆小幣名稱
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料sql語法
        command = "SELECT  `symbol_name` FROM symbol_data_table"

        # 執行指令
        cursor.execute(command)

        # 取得第一筆資料
        result_for_one = cursor.fetchone()

        print("查詢單筆資料成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
result_for_one

# %%
# 查詢特定筆數的小幣名稱
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料sql語法
        command = "SELECT  `symbol_name` FROM symbol_data_table"

        # 執行指令
        cursor.execute(command)

        # 取得第一筆資料
        result_for_many = cursor.fetchmany(5)

        print("查詢多筆資料成功")
        conn.close()
except Exception as ex:
    print(ex)
# %%
result_for_many

# %%
# 條件查詢小幣名稱
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 新增資料sql語法
        command = "SELECT  `symbol_name` FROM symbol_data_table WHERE symbol_name = %s"

        # 執行指令
        cursor.execute(command, ("BTCUSDT"))

        # 取得第一筆資料
        result_for_where = cursor.fetchall()

        print("條件查詢全部資料成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
result_for_where
# %%
# 修改特定小幣名稱
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 修改資料SQL語法
        command = "UPDATE symbol_data_table SET symbol_name = %s WHERE symbol_name = %s"

        # 執行指令
        cursor.execute(command, ("SHIBUSDT", "SHIBUDT"))

        # 儲存變更
        conn.commit()

        print("修改資料成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
# 刪除特定小幣名稱
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 修改資料SQL語法
        command = "DELETE FROM symbol_data_table WHERE symbol_name = %s"

        # 執行指令
        cursor.execute(command, ("SHIBUSDT"))

        # 儲存變更
        conn.commit()

        print("刪除資料成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
