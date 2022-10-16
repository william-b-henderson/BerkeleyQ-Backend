from app import app
import os
import pymysql
from flask import request

conn = pymysql.connect(
        host= os.getenv('MYSQL_DATABASE_HOST'), 
        port = os.getenv('MYSQL_DATABASE_PORT'),
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
    return class_names

@app.route('/class', methods=['POST'])
def post_class():
    return "put class in classes table"

@app.route('/schedule/<class_id>')
def get_class_schedule(class_id):
    return "Class schedule for class_id {}".format(class_id)

@app.route('/oh/<class_id>/<oh_id>')
def get_class_oh(class_id, oh_id):
    return "OH {} for class {}".format(oh_id, class_id)

{}