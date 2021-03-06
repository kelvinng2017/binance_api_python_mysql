# %%
import pymysql
import configparser
import time
from datetime import datetime
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
    conn = pymysql.connect(**db_settings_for_high_hand)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 刪除資料表指令
        command = "DROP TABLE  `%s`"

        # 執行指令
        cursor.execute(command, ('2021-07-28 16:22:22'))

        print("刪除資料表成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings_for_high_hand)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 刪除資料表指令
        show_table_sql = "SHOW TABLES"

        # 執行指令
        cursor.execute(show_table_sql)
        result_for_all = cursor.fetchall()

        print(result_for_all)
        conn.close()
except Exception as ex:
    print(ex)

# %%
eval(result_for_all[1][0])

# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings_for_high_hand)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 刪除資料表指令
        command = "DROP TABLE  `%s`"

        # 執行指令
        for result_for_all_index in range(len(result_for_all)):
            cursor.execute(command, (eval(result_for_all[result_for_all_index][0])
                                     ))

        print("刪除資料表成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
abc = "apple"
now = datetime.now()

# %%
datetime.now().microsecond
# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 建立資料表指令
        for i in range(1):
            sql = "CREATE TABLE symbol_data_table(symbol_id INT NOT NULL AUTO_INCREMENT, symbol_name VARCHAR(100) NOT NULL ,PRIMARY KEY(symbol_id))"
            cursor.execute(sql)
        conn.commit()
        print("建立資料表成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 修改資料表名稱指令
        command = "ALTER TABLE symbol_data_table1 RENAME TO symbol_data_table;"

        # 執行指令
        cursor.execute(command)

        print("修改資料表名稱成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
now_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())
print(now_time)
# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings_for_high_hand_table_name)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 建立資料表指令
        command_create_datatable = "create  table name_table(table_name_id INT(255) NOT NULL AUTO_INCREMENT,table_name VARCHAR(100) NOT NULL,PRIMARY KEY(table_name_id))"

        # 執行指令
        cursor.execute(command_create_datatable)

        print("建立資料表成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
