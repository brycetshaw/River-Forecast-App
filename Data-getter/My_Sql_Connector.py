import csv
from itertools import islice

import mysql
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import os
import pytz


def create_db_connection():
    try:
        print("trying")
        # TODO Create ENV variables to handle database credentials in a correct way.
        # I think I need to use https://direnv.net/
        # db_host = env(DB_HOST, 'localhost')
        # db_port = env.int(DB_PORT, 3306)
        # db_user = env(DB_USER)
        # db_pass = env(DB_PASS)
        # db_name = env(DB_NAME)
        #
        # conn = pymysql.connect(db_host,db_user,db_pass,db_name, use_unicode=True, charset="utf8")

        # connection = mysql.connector.connect(host='162.246.156.171',
        #                                      database='riverapp',
        #                                      user='riverapp',
        #                                      password='riverapp',
        #                                      auth_plugin='mysql_native_password')
        # connection = mysql.connector.connect(host='localhost',
        #                                      )
        connection = mysql.connector.connect(host='localhost',
                                             database='riverapp',
                                             user='riverapp',
                                             password='riverapp',
                                             auth_plugin='mysql_native_password')
        print("connection attempted")
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            cursor.close()
            print(f"You're connected to database: {record}")
            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)


def add_sensor_types(db_connection, type_name, type_def):
    print('hello')


def return_sensor_fields(db_connection, type_name):
    # Requires: DB connection object & type_name string
    # returns: array of fields which store
    sql = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{type_name}'"


def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{tablename}'")
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


# def addData(db_connection, sensortag, data, data_type):
#     if not checkTableExists(db_connection, sensortag):
#         db_cursor = db_connection.cursor()
#         db_cursor.excecute(f"")
#         sql = f"INSERT INTO "


def create_data_group_table(db_connection):
    if not checkTableExists(db_connection, 'data_group'):
        sql = f"CREATE TABLE IF NOT EXISTS data_group (" \
              f"entry_id INT AUTO_INCREMENT PRIMARY KEY," \
              f"sensor_id VARCHAR(255) NOT NULL," \
              f"data_group_id VARCHAR(255)," \
              f"table_type VARCHAR(255) NOT NULL," \
              f"start_date DATETIME," \
              f"end_date DATETIME" \
              f")"
        cursor = db_connection.cursor()
        cursor.execute(sql)
        print("created data group table")
    else:
        print("data group table exists.")


def add_sensor_table(db_connection, sensor_id, data_group_id, table_type):
    # Creates a table (if a table with the label of sensor_id doesn't already exist)
    # and adds a row into the datagroup table with the sensor details.
    sql = f"CREATE TABLE IF NOT EXISTS {sensor_id} (" \
          f"time DATETIME NOT NULL PRIMARY KEY," \
          f"flowrate DOUBLE," \
          f"gauge_height DOUBLE" \
          f")"

    sql2 = f"INSERT INTO data_group (sensor_id, data_group_id, table_type)" \
           f"VALUES ('{sensor_id}', '{data_group_id}', '{table_type}')"

    if checkTableExists(db_connection, sensor_id):
        print(f"table {sensor_id} already exists")
        return

    try:
        cursor = db_connection.cursor()
        cursor.execute(sql)
        cursor.execute(sql2)
        db_connection.commit()

    except Error as e:
        print("Error while executing query\n", sql, e)


def add_snow_sensor_table(db_connection, sensor_id, data_group_id, table_type):

    sql = f"CREATE TABLE IF NOT EXISTS {sensor_id} (" \
          f"time DATETIME NOT NULL PRIMARY KEY," \
          f"height DOUBLE," \
          f"temperature_at_snowpillow DOUBLE" \
          f")"

    sql2 = f"INSERT INTO data_group (sensor_id, data_group_id, table_type)" \
           f"VALUES ('{sensor_id}', '{data_group_id}', '{table_type}')"

    if checkTableExists(db_connection, sensor_id):
        print(f"table {sensor_id} already exists")
        return

    try:
        cursor = db_connection.cursor()
        cursor.execute(sql)
        cursor.execute(sql2)
        db_connection.commit()

    except Error as e:
        print("Error while executing query\n", sql, e)


def add_flow_value(cursor, sensor_id, timestamp, flow_rate):
    sql = f"INSERT INTO {sensor_id} (time, flowrate)" \
          f"VALUES ('{pd.to_datetime(timestamp).strftime('%Y-%m-%d %H:%M:%S')}', {flow_rate})"
    try:
        cursor.execute(sql)
    except Error as e:
        print("Error while executing query\n", sql, e)


def add_snow_value(cursor, sensor_id, timestamp, height, temperature):
    sql = f"INSERT INTO {sensor_id} (time, height, temperature_at_snowpillow)" \
          f"VALUES ('{pd.to_datetime(timestamp).strftime('%Y-%m-%d %H:%M:%S')}', {height}, {temperature})"
    try:
        cursor.execute(sql)
    except Error as e:
        print("Error while executing query\n", sql, e)


def get_row_col(csv_filename, row, col):
    with open(csv_filename, 'rt') as f:
        return next(islice(csv.reader(f), row, row + 1))[col]


def import_river_from_csv(db_connection):
    flow_csv_path = '../Data/Spillimacheen/08NA011_QR_Apr-2-2020_06_01_41PM.csv'
    # flow_csv_path = '../Data/Spillimacheen/smaller_river_test_set.csv'

    flow_df_raw = pd.read_csv(flow_csv_path, header=7, index_col=0)
    flow_df_raw.drop(["Parameter "], axis=1, inplace=True)
    flow_df_raw.index = pd.to_datetime(flow_df_raw.index)

    flow = pd.DataFrame()
    flow['flow {m3/s)'] = flow_df_raw['Value (m3/s)'].resample('H').first()
    cursor = db_connection.cursor()

    data_group_id = get_row_col(flow_csv_path, 5, 1)
    sensor_id = get_row_col(flow_csv_path, 5, 0)
    table_type = 'flow'
    add_sensor_table(db_connection, sensor_id, data_group_id, table_type)
    for index, row in flow.iterrows():
        if pd.isna(row[0]) or pd.isna(index):
            continue
        add_flow_value(cursor, sensor_id, index, row[0])
    db_connection.commit()
    return data_group_id

    # flow.to_sql(con=db_connection, if_exists='replace', flavor='mysql')


def import_snowpack_from_csv(db_connection):
    df_snow = pd.DataFrame()
    folder_to_loop = "../Data/Spillimacheen/snow-pillow-conrad-glacier"
    for root, dirs, files in os.walk(folder_to_loop):
        for filename in files:
            temp = pd.read_csv(folder_to_loop + '/' + filename, header=2, index_col=0)
            temp.index = pd.to_datetime(temp.index)
            temp = temp.iloc[:, 0:1]
            print(temp.columns[0])
            if len(df_snow) == 0:
                df_snow = temp
            df_snow = pd.concat([df_snow, temp], axis=1)

    df_snow = df_snow[['Value (Celsius)', 'Value (Centimetres)']].dropna()
    print(df_snow.head(10))

    flow_csv_path = '../Data/Spillimacheen/08NA011_QR_Apr-2-2020_06_01_41PM.csv'
    # flow_csv_path = '../Data/Spillimacheen/smaller_river_test_set.csv'

    cursor = db_connection.cursor()

    data_group_id = get_row_col(flow_csv_path, 5, 1)
    sensor_id = '2A33P'
    table_type = 'snow-pillow'
    # add_sensor_table(db_connection, sensor_id, data_group_id, table_type)
    add_snow_sensor_table(db_connection, sensor_id, data_group_id, table_type)
    for index, row in df_snow.iterrows():
        if pd.isna(row[1]) or pd.isna(index):
            print("is error")
            continue
        add_snow_value(cursor, sensor_id, index, row[1], row[0])
    db_connection.commit()
    return data_group_id


def get_sensors(db_connection):
    sql = "select sensor_id from data_group"

    cursor = db_connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return [x[0] for x in result]

# TODO sensor bound needs to populate data group start and end date fields.
def get_sensor_bound(db_connection, sensor):
    sql1 = f"SELECT MAX(time) from {sensor}"
    sql2 = f"SELECT MIN(time) from {sensor}"
    cursor = db_connection.cursor()
    cursor.execute(sql1)
    result = cursor.fetchall()
    cursor.execute(sql2)
    result.append(cursor.fetchall())
    cursor.close()
    return [x[0] for x in result]

def populate_data_group_bounds(db_connection):
    db_connection = create_db_connection()
    cursor = db_connection.cursor()
    sensors = get_sensors(db_connection)
    result = pd.DataFrame()
    for sensor in sensors:
        temp = get_sensor_bound(db_connection, sensor)
        print(temp)




def main():
    # This file is ugly, but it populates a database

    db_connection = create_db_connection()
    create_data_group_table(db_connection)
    data_group_id = import_river_from_csv(db_connection)
    import_snowpack_from_csv(db_connection)
    populate_data_group_bounds(db_connection)
    if db_connection.is_connected():
        db_connection.close()
        print("MySQL connection is closed")


if __name__ == '__main__':
    main()
