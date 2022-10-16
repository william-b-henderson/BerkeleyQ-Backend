from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/classes')
def get_classes():
    return "Classes"

@app.route('/schedule/<class_id>')
def get_class_schedule(class_id):
    return "Class schedule for class_id {}".format(class_id)

@app.route('/oh/<class_id>/<oh_id>')
def get_class_oh(class_id, oh_id):
    return "OH {} for class {}".format(oh_id, class_id)
