
"""
    Main file for the RESTful API built as a part of coding challange from kiwiki.
"""

from datetime import datetime, timedelta
from flask import Flask, request, render_template
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy

import logging
logging.basicConfig(filename="webapp.log")

app = Flask(__name__)
app.config['APP_SETTINGS'] = DevelopmentConfig
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/kiwi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import DeviceHealth


"""
    App route for landing page

    Method:
        GET

    Input:

    Output:
"""


@app.route('/')
def index():
    return render_template('index.html')


"""
    App route for view 1 of the report

    Method:
        GET, POST

    Input(GET):

    Input(POST):
        date: string (format: YY-MM-DD)

    Output:
        list: list of lists containing
                    [device_id,
                     no. of occurrence of given date,
                     no. of occurrence at 7 days ago,
                     percentage of change of occurrence in a week
                     ]
"""


@app.route('/reports/view_1', methods=["GET", "POST"])
def view_1():
    if request.method == "POST":
        try:
            selected_date = request.form['datepicker']

            selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')
            seven_days_ago = str(selected_datetime - timedelta(days=7)).split(' ')[0]

            packed = db.session.query(DeviceHealth).with_entities(DeviceHealth.device_id,
                                                                  db.func.count(DeviceHealth.device_id)).\
                filter_by(date_created=selected_date).group_by(DeviceHealth.device_id).\
                order_by(db.func.count(DeviceHealth.device_id).desc()).limit(10)

            packed_data = [[each[0], each[1]] for each in packed]

            for each in packed_data:
                last_week_count = db.session.query(DeviceHealth).filter_by(date_created=seven_days_ago, device_id=each[0]).count()
                if last_week_count != 0:
                    percentage_of_change = ((float(each[1]) - float(last_week_count)) / float(last_week_count)) * 100
                else:
                    percentage_of_change = float(each[1]) * 100
                each.append(last_week_count)
                each.append(round(percentage_of_change, 2))
        except Exception as exp:
            logging.log(40, exp)
            return render_template('page_1.html', landing=True)
        return render_template('page_1.html', data=packed_data, date=selected_date)
    return render_template('page_1.html', landing=True)


"""
    App route for view 2 of the report

    Method:
        GET, POST

    Input(GET):

    Input(POST):
        device_type: string
        status: string

    Output:
        list: list of lists containing
                    [date_created,
                     no. of total devices for each day
                    ]
"""


@app.route('/reports/view_2', methods=["GET", "POST"])
def view_2():
    # import pdb; pdb.set_trace()
    if request.method == "POST":
        try:
            filter_dict = dict()
            if request.form['device_type'] != "":
                filter_dict['device_type'] = request.form['device_type']
            if request.form['status'] != "":
                filter_dict['status'] = request.form['status']

            # Hardcoded date range(to, from) due to the lack of given data. Should be automated in real system.
            date_to = "2017-05-13"
            date_from = "2017-04-13"

            filtered_data = db.session.query(DeviceHealth).with_entities(
                DeviceHealth.date_created, db.func.count(DeviceHealth.device_id)).\
                filter(DeviceHealth.date_created >= date_from).filter(DeviceHealth.date_created <= date_to).\
                filter_by(**filter_dict).\
                group_by(DeviceHealth.date_created).\
                order_by(DeviceHealth.date_created.desc())
        except Exception as exp:
            logging.log(40, exp)
            return render_template('page_2.html', landing=True)
        return render_template('page_2.html', data=filtered_data)
    return render_template('page_2.html', landing=True)

if __name__ == '__main__':
    app.run(debug=True)
