import os
from dotenv import load_dotenv
import pymysql
from flask import request
from http import HTTPStatus
import datetime
import json


from flask import Flask
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# conn = pymysql.connect(
#         host= os.getenv('MYSQL_DATABASE_HOST'), 
#         port = int(os.getenv('MYSQL_DATABASE_PORT')),
#         user = os.getenv('MYSQL_DATABASE_USER'), 
#         password = os.getenv('MYSQL_DATABASE_PASSWORD'),
#         db = os.getenv('MYSQL_DATABASE_NAME'),
#         )
# cursor = conn.cursor()

conn = pymysql.connect(
        host= 'berkeleyq-mysql.cj1vstpo0icf.us-west-2.rds.amazonaws.com', 
        port = int(3306),
        user = 'berkeleyq_admin', 
        password = 'uIrOPIjHYVhkbQZ55iFD',
        db = 'berkeleyq_mysql',
        )
cursor = conn.cursor()

def datetime_handler(x):
    if isinstance(x, datetime.timedelta):
        return str(x)
    return x



@app.route('/')
@app.route('/index')
def index():
    return "Welcome to our project!"

@app.route('/classes')
def get_classes():
    get_classes = """
        SELECT * FROM classes;
        """
    cursor.execute(get_classes)
    class_names = cursor.fetchall()
    print(f"Class Names, {class_names}")
    return list(class_names), HTTPStatus.OK

@app.route('/class', methods=['POST'])
def post_class():
    query_params = request.args.to_dict()
    class_id = query_params.get("class-id")
    class_name = query_params.get("class-name")
    insert_class = """
        INSERT INTO classes 
        VALUES (%s, %s);
        """
    cursor.execute(insert_class, (class_id, class_name))
    conn.commit()
    return "Class placed in table", HTTPStatus.OK

@app.route('/schedule/<class_id>')
def get_class_schedule(class_id):
    get_schedule = """
        SELECT * FROM schedule WHERE class_id=%s;
    """
    cursor.execute(get_schedule, (class_id))
    schedule = cursor.fetchall()
    return json.dumps(schedule, default=datetime_handler), HTTPStatus.OK

@app.route('/oh', methods=['POST'])
def post_oh():
    query_params = request.json
    class_id = query_params.get("class_id")
    oh_id = query_params.get("oh_id")
    timestamp = query_params.get("timestamp")
    wait_time = query_params.get("wait_time")
    num_open_tickets = query_params.get("num_open_tickets")
    num_tas_online = query_params.get("num_tas_online")
    num_people_online = query_params.get("num_people_online")
    insert_oh = """
    INSERT INTO oh
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_oh, (class_id, oh_id, timestamp, wait_time, num_open_tickets, num_tas_online, num_people_online))
    conn.commit()
    return "OH placed in table", HTTPStatus.OK

@app.route('/oh/stats/avg_wait_time', methods=['GET'])
def get_average_wait_time():
    query_params = request.args.to_dict()
    class_id = query_params.get("class_id")
    oh_id = query_params.get("oh_id")
    start_time = query_params.get("start_time")
    end_time = query_params.get("end_time")
    if start_time is not None and end_time is not None:
        get_average_wait_time = """
        SELECT AVG(wait_time) FROM oh
        WHERE class_id=%s AND oh_id=%s AND timestamp>=%s AND timestamp<=%s
        """
        cursor.execute(get_average_wait_time, (class_id, oh_id, start_time, end_time))
        avg_wait_time = cursor.fetchall()
        return str(avg_wait_time), HTTPStatus.OK

    get_average_wait_time ="""
    SELECT AVG(wait_time) FROM oh
    WHERE class_id=%s AND oh_id=%s
    """
    cursor.execute(get_average_wait_time, (class_id, oh_id,))
    avg_wait_time = cursor.fetchall()
    return str(avg_wait_time), HTTPStatus.OK

@app.route('/oh/stats/avg_num_open_tickets', methods=['GET'])
def get_average_num_open_tickets():
    query_params = request.args.to_dict()
    class_id = query_params.get("class_id")
    oh_id = query_params.get("oh_id")
    start_time = query_params.get("start_time")
    end_time = query_params.get("end_time")
    if start_time is not None and end_time is not None:
        get_average_num_open_tickets = """
        SELECT AVG(num_open_tickets) FROM oh
        WHERE class_id=%s AND oh_id=%s AND timestamp>=%s AND timestamp<=%s
        """
        cursor.execute(get_average_num_open_tickets, (class_id, oh_id, start_time, end_time))
        avg_num_open_tickets = cursor.fetchall()
        return str(avg_num_open_tickets), HTTPStatus.OK

    get_average_num_open_tickets ="""
    SELECT AVG(num_open_tickets) FROM oh
    WHERE class_id=%s AND oh_id=%s
    """
    cursor.execute(get_average_num_open_tickets, (class_id, oh_id,))
    avg_num_open_tickets = cursor.fetchall()
    return str(avg_num_open_tickets), HTTPStatus.OK

@app.route('/oh/stats/avg_num_people_online', methods=['GET'])
def get_average_num_people_online():
    query_params = request.args.to_dict()
    class_id = query_params.get("class_id")
    oh_id = query_params.get("oh_id")
    start_time = query_params.get("start_time")
    end_time = query_params.get("end_time")
    if start_time is not None and end_time is not None:
        get_average_num_people_online = """
        SELECT AVG(num_people_online) FROM oh
        WHERE class_id=%s AND oh_id=%s AND timestamp>=%s AND timestamp<=%s
        """
        cursor.execute(get_average_num_people_online, (class_id, oh_id, start_time, end_time))
        avg_num_people_online = cursor.fetchall()
        return str(avg_num_people_online), HTTPStatus.OK

    get_average_num_people_online ="""
    SELECT AVG(num_people_online) FROM oh
    WHERE class_id=%s AND oh_id=%s
    """
    cursor.execute(get_average_num_people_online, (class_id, oh_id,))
    avg_num_people_online = cursor.fetchall()
    return str(avg_num_people_online), HTTPStatus.OK

@app.route('/oh/stats/max_num_tas_online', methods=['GET'])
def get_max_num_tas_online():
    query_params = request.args.to_dict()
    class_id = query_params.get("class_id")
    oh_id = query_params.get("oh_id")
    start_time = query_params.get("start_time")
    end_time = query_params.get("end_time")
    if start_time is not None and end_time is not None:
        get_max_num_tas_online = """
        SELECT MAX(num_tas_online) FROM oh
        WHERE class_id=%s AND oh_id=%s AND timestamp>=%s AND timestamp<=%s
        """
        cursor.execute(get_max_num_tas_online, (class_id, oh_id, start_time, end_time))
        max_num_tas_online = cursor.fetchall()
        return str(max_num_tas_online), HTTPStatus.OK

    get_max_num_tas_online ="""
    SELECT MAX(num_tas_online) FROM oh
    WHERE class_id=%s AND oh_id=%s
    """
    cursor.execute(get_max_num_tas_online, (class_id, oh_id,))
    max_num_tas_online = cursor.fetchall()
    return str(max_num_tas_online), HTTPStatus.OK