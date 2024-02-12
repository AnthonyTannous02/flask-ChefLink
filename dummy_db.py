from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dummy.db'
db = SQLAlchemy(app)

class DummyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

@app.route('/add', methods=['POST'])
def add_data():
    name = request.form.get('name')
    age = request.form.get('age')
    data = DummyData(name, age)
    db.session.add(data)
    db.session.commit()
    return 'Data added successfully'

@app.route('/update', methods=['POST'])
def update_data():
    id = request.form.get('id')
    name = request.form.get('name')
    age = request.form.get('age')
    data = DummyData.query.get(id)
    if data:
        data.name = name
        data.age = age
        db.session.commit()
        return 'Data updated successfully'
    else:
        return 'Data not found'

@app.route('/get', methods=['GET'])
def get_data():
    id = request.args.get('id')
    data = DummyData.query.get(id)
    if data:
        return f"Name: {data.name}, Age: {data.age}"
    else:
        return 'Data not found'

if __name__ == '__main__':
    db.create_all()
    app.run()