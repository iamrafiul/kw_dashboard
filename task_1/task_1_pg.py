import csv
import os
from postgres import Postgres
import logging
logging.basicConfig(filename="script.log")

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
    try:
        sql = 'INSERT INTO device_health (date_created, device_id, device_type, status) VALUES(%(date_created)s, %(device_id)s, %(device_type)s, %(status)s)'
        db.run(sql, {'date_created': each[0], 'device_id': each[1], 'device_type': each[2], 'status': each[3]})
    except Exception as exp:
        logging.log(40, exp)
