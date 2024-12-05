
from flask import Flask, render_template, request, redirect, jsonify

from utils.db import db

from models.student import *


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Student.db'

@app.route('/')
def index():
    student = Student.query.all()
    return render_template('index.html',  content=student)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_student')
def add_student():
    return render_template('add_student.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    id = form_data.get('id')
    name = form_data.get('name')
    maths = form_data.get('maths')
    biology = form_data.get('biology')
    social = form_data.get('social')
    percentage = form_data.get('percentage')

    student = Student.query.filter_by(id=id).first()
    if not student:
        student = Student(id=id, name=name, maths=maths, biology=biology, social=social, percentage=percentage)
        db.session.add(student)
        db.session.commit()
    print("sumitted successfully")
    return redirect('/')



@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete(id):
    student = Student.query.get(id)
    print("task: {}".format(student))

    if not student:
        return jsonify({'message': 'student not found'}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'student deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


if __name__ =='__main__':
    app.run(host='127.0.0.1',port=5003,debug=True)
