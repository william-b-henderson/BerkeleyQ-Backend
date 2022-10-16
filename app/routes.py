from app import app
import os
import pymysql
from flask import request
from http import HTTPStatus

conn = pymysql.connect(
        host= os.getenv('MYSQL_DATABASE_HOST'), 
        port = int(os.getenv('MYSQL_DATABASE_PORT')),
        user = os.getenv('MYSQL_DATABASE_USER'), 
        password = os.getenv('MYSQL_DATABASE_PASSWORD'),
        db = os.getenv('MYSQL_DATABASE_NAME'),
        )
cursor = conn.cursor()



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
    return "Class schedule for class_id {}".format(class_id)

@app.route('/oh/<class_id>/<oh_id>')
def get_class_oh(class_id, oh_id):
    return "OH {} for class {}".format(oh_id, class_id)
