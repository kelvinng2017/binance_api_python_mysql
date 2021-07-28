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
    "db": config['database_settings']['db'],
    "charset": config['database_settings']['charset']
}
# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 刪除資料表指令
        command = "DROP TABLE symbol_data_table"

        # 執行指令
        cursor.execute(command)

        print("刪除資料表成功")
        conn.close()
except Exception as ex:
    print(ex)

# %%
# %%
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)

    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 建立資料表指令
        command = "CREATE TABLE symbol_data_table(symbol_id INT NOT NULL AUTO_INCREMENT, symbol_name VARCHAR(100) NOT NULL ,PRIMARY KEY(symbol_id));"

        # 執行指令
        cursor.execute(command)

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
