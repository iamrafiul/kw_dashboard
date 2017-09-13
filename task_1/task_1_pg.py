# @Author: mdrhri-6
# @Date:   2017-09-03T22:49:22+02:00
# @Last modified by:   mdrhri-6
# @Last modified time: 2017-09-03T21:10:07+02:00

import csv
import os
from postgres import Postgres

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

db = Postgres("postgres://localhost/kiwi")

db.run('create table device_health(id serial primary key not null, device_id text, device_type text, status text, date_created date default null)')

def get_csv_data(filename):
    CSV_PATH = os.path.join(ROOT_PATH, filename)
    with open(CSV_PATH, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_reader.next()
        for row in csv_reader:
            yield row

for each in get_csv_data('report.csv'):
    sql = 'INSERT INTO device_health (date_created, device_id, device_type, status) VALUES(%(date_created)s, %(device_id)s, %(device_type)s, %(status)s)'
    db.run(sql, {'date_created': each[0], 'device_id': each[1], 'device_type': each[2], 'status': each[3]})
