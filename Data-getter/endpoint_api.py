import csv
from itertools import islice

import mysql
from mysql.connector import Error
import pandas as pd
import datetime
import os
import pytz
import re


def create_db_connection():
    print('get data connection')
    try:

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

        connection = mysql.connector.connect(host='localhost',
                                             database='riverapp',
                                             user='riverapp',
                                             password='riverapp',
                                             auth_plugin='mysql_native_password')
        print('maybe got connection')

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


def get_sensors_in_datagroup(db_connection, datagroup):
    sql = f"select sensor_id from data_group where data_group_id='{datagroup}'"
    cursor = db_connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return [x[0] for x in result]


def query_sensor(db_connection, sensor, start, end):
    sql = f"SELECT * from {sensor} WHERE time > '{start}' && time < '{end}'"
    return pd.read_sql(sql, db_connection)


def get_sensor_list(db_connection, data_group):
    sql = f"SELECT * FROM data_group WHERE data_group_id == '{data_group}'"

    cursor = db_connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return [x[0] for x in result]
    # return pd.read_sql(sql, create_db_connection()).to_csv(index=False)


def query_database(data_group, start_time, end_time):
    # Front End API
    try:
        if not isinstance(start_time, datetime.date):
            start_time = datetime.datetime.fromtimestamp(int(start_time) / 1E3)
            end_time = datetime.datetime.fromtimestamp(int(end_time) / 1E3)
    except:
        print("caught a datetime conversion error. this is expected")

    db_connection = create_db_connection()
    sensors = get_sensors_in_datagroup(db_connection, data_group)
    result = pd.DataFrame()
    for sensor in sensors:
        temp = query_sensor(db_connection, sensor, start_time, end_time)
        temp.index = temp['time']
        if result.size is 0:
            result = temp
        result = result.merge(temp, how='outer', left_index=True, right_index=True, suffixes=('', '_y'))
        result.drop(list(result.filter(regex='_y$')), axis=1, inplace=True)
    db_connection.close()
    return result.to_json(orient='split', index=False)


def get_sensors_list(datagroup):
    # Front end API
    sql = f"select sensor_id, start_date, end_date from data_group where data_group_id='{datagroup}'"
    db_connection = create_db_connection()
    result = pd.read_sql(sql, db_connection).drop_duplicates().to_json(orient='split', index=False)
    db_connection.close()
    return result


def get_datagroups():
    # Front End API
    sql = f"select data_group_id from data_group"
    db_connection = create_db_connection()
    result = pd.read_sql(sql, db_connection).drop_duplicates().to_json(orient='split', index=False)
    db_connection.close()
    return result


def main():
    print(get_datagroups())

    print(get_sensors_list("SPILLIMACHEEN RIVER NEAR SPILLIMACHEEN"))
    result = query_database("SPILLIMACHEEN RIVER NEAR SPILLIMACHEEN", '2020-02-15 19:00:00', '2020-02-19 17:00:00')
    print(result)


if __name__ == '__main__':
    main()
