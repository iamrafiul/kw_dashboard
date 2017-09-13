# @Author: mdrhri-6
# @Date:   2017-08-28T22:49:22+02:00
# @Last modified by:   mdrhri-6
# @Last modified time: 2017-09-03T18:26:43+02:00

import csv
import os
import sqlite3


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect('kiwi.db')

c = conn.cursor()

c.execute('DROP TABLE IF EXISTS device_health')


# create table device_health(id int, device_id text, device_type text, status text, date_created timestamp)   
c.execute('CREATE TABLE device_health (date_created text, device_id text, device_type text, status text)')

def get_csv_data(filename):
    CSV_PATH = os.path.join(ROOT_PATH, filename)
    with open(CSV_PATH, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_reader.next()
        for row in csv_reader:
            yield row
count = 0
for each in get_csv_data('report.csv'):
    sql = 'INSERT INTO device_health (date_created, device_id, device_type, status) VALUES(?,?,?,?)'
    c.execute(sql, (each[0], each[1], each[2], each[3]))
    conn.commit()
    count += 1
    print count
