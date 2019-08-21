import os, csv
from flask import Flask, request, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Should I create a global fields tuple??
#fields = ('first', 'last', 'position', 'email', 'location', 'ringCentral', 'workPhone', 'mobilePhone')

# Employee Class and Constructor
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(50))
    last = db.Column(db.String(50))
    position = db.Column(db.String(50))
    email = db.Column(db.String(50))
    location = db.Column(db.String(50))
    ringCentral = db.Column(db.Integer)
    workPhone = db.Column(db.Integer)
    mobilePhone = db.Column(db.Integer)

    def __init__(self, first, last, position, email, location, ringCentral, workPhone, mobilePhone):
        self.first = first
        self.last = last
        self.position = position
        self.email = email
        self.location = location
        self.ringCentral = ringCentral
        self.workPhone = workPhone
        self.mobilePhone = mobilePhone

# Employee Schema
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first', 'last', 'position', 'email', 'location', 'ringCentral', 'workPhone', 'mobilePhone')
        #fields = fields

#Init Schema
employee_schema = EmployeeSchema(strict=True)
employees_schema = EmployeeSchema(many=True, strict=True)

#Create Employee
@app.route('/employee', methods=['POST'])
def add_employee():
    first = request.json['first'] #first = request.json[fields[0]]
    last = request.json['last']
    position = request.json['position']
    email = request.json['email']
    location = request.json['location']
    ringCentral = request.json['ringCentral']
    workPhone = request.json['workPhone']
    mobilePhone = request.json['mobilePhone']

    new_employee = Employee(first, last, position, email, location, ringCentral, workPhone, mobilePhone)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)
           
#Create Employees from CSV
@app.route('/index')
def index():
    return render_template('upload.html')

@app.route('/upload_employees', methods=['POST'])
def upload():
    file = request.files['inputFile'].read().decode('utf8').split('\n')
    reader = csv.DictReader(file, delimiter=',')

    fields = ('first', 'last', 'position', 'email', 'location', 'ringCentral', 'workPhone', 'mobilePhone')

    for row in reader:

        # Find empty fields in CSV:
        for val in fields:
            if row[val] is "":
                row[val] = None

        first = row['first'] #first = row[fields[0]]
        last = row['last']
        position = row['position']
        email = row['email']
        location = row['location']
        ringCentral = row['ringCentral']
        workPhone = row['workPhone']
        mobilePhone = row['mobilePhone']

        new_employee = Employee(first, last, position, email, location, ringCentral, workPhone, mobilePhone)

        db.session.add(new_employee)
        db.session.commit()
        
    return '<h1>CSV Successfully Parsed</h1>'

# Get Single Employee
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)

# Get All Employees
@app.route('/employee', methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result.data)

# Update Employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    first = request.json['first'] #first = request.json[fields[0]]
    last = request.json['last']
    position = request.json['position']
    email = request.json['email']
    location = request.json['location']
    ringCentral = request.json['ringCentral']
    workPhone = request.json['workPhone']
    mobilePhone = request.json['mobilePhone']

    employee.first = first
    employee.last = last
    employee.position = position
    employee.email = email
    employee.location = location
    employee.ringCentral = ringCentral
    employee.workPhone = workPhone
    employee.mobilePhone = mobilePhone

    db.session.commit()

    return employee_schema.jsonify(employee)

# Delete Employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)