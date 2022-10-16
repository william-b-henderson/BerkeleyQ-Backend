from app import app
import os
import pymysql
from flask import request
from http import HTTPStatus
import datetime
import json

conn = pymysql.connect(
        host= os.getenv('MYSQL_DATABASE_HOST'), 
        port = int(os.getenv('MYSQL_DATABASE_PORT')),
        user = os.getenv('MYSQL_DATABASE_USER'), 
        password = os.getenv('MYSQL_DATABASE_PASSWORD'),
        db = os.getenv('MYSQL_DATABASE_NAME'),
        )
cursor = conn.cursor()

def datetime_handler(x):
    if isinstance(x, datetime.timedelta):
        return str(x)
    return x



@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/classes')
def get_classes():
    get_classes = """
        SELECT DISTINCT(class_name) FROM classes;
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

@app.route('/oh/<class_id>/<oh_id>', methods=['GET'])
def get_average_wait_time(class_id, oh_id):
    get_average_wait_time ="""
    SELECT AVG(wait_time) FROM oh
    WHERE class_id=%s AND oh_id=%s
    """
    cursor.execute(get_average_wait_time, (class_id, oh_id))
    avg_wait_time = cursor.fetchall()
    return str(avg_wait_time), HTTPStatus.OK
