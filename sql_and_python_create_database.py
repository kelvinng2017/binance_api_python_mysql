# %%
import pymysql
import configparser
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
    "charset": config['database_settings']['charset']
}

# %%
db_settings_for_high_hand = {
    "host": config['database_settings']['host'],
    "port": int(config['database_settings']['port']),
    "user": config['database_settings']['user'],
    "password": config['database_settings']['password'],
    "charset": config['database_settings']['charset']
}
# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings_for_high_hand)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 刪除資料表指令
        command = "create database tabel_name"

        # 執行指令
        cursor.execute(command)

        print("建立資料庫成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 顯示MarialDB10 有幾個資料庫
        command = "show databases"

        # 執行指令
        cursor.execute(command)
        result_of_database_name = cursor.fetchall()
        print(result_of_database_name)
        print("顯示MarialDB10 有幾個資料庫成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 刪除特定的資料庫
        command = "drop database binance_data_base"

        # 執行指令
        cursor.execute(command)

        print("刪除料庫成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
""""
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 刪除特定的資料庫
        command = "RENAME DATABASE 'binance_data_base' TO 'binance_database'"

        # 執行指令
        cursor.execute(command)

        print("刪除料庫成功")
        conn.close()
except Exception as ex:
    print(ex)
"""

# %%
