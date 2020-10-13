import os, csv
from pprint import pprint
from flask import Flask, request, jsonify, render_template
from marshmallow import Schema, fields, post_load, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init employee database
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)

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
class EmployeeSchema(Schema):
    first = fields.String()
    last = fields.String()
    position = fields.String()
    email = fields.Email()
    location = fields.String()
    ringCentral = fields.Integer(allow_none=True)
    workPhone = fields.Integer(allow_none=True)
    mobilePhone = fields.Integer(allow_none=True)

    class Meta:
        fields = ('id', 'first', 'last', 'position', 'email', 'location', 'ringCentral', 'workPhone', 'mobilePhone') 

    @post_load
    def create_employee(self, data, **kwargs):
        return Employee(**data)

#Init Schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# homepage
@app.route('/index') 
def index():
    return render_template('upload.html')

#Create Employee
@app.route('/create_employee', methods=['POST'])
def add_employee():
    first = request.json['first'] 
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

    return "<h1>SUCCESS</h1>"
           
def allowed_file(filename):
    allowedExtensions = {'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtensions

#Create Employees from CSV
@app.route('/upload_employees', methods=['POST'])
def upload():
    file = request.files['inputFile']

    # If no file selected
    if file.filename == '':
        return '<h1>No file selected</h1>'

    # Filetype check
    if file and allowed_file(file.filename):

        # Read in values from CSV:
        csvFile = file.read().decode().split('\n')
        reader = csv.DictReader(csvFile, delimiter=',')

        fields = ('first', 'last', 'position', 'email', 'location', 'ringCentral', 'workPhone', 'mobilePhone')

        for row in reader:

            # Find empty fields in CSV:
            for val in fields:
                if row[val] is "":
                    row[val] = None

            # Schema Validation:
            try:
                new_employee = employee_schema.load(dict(row))
            except ValidationError as err:
                print(row['first'] + ' ' + row['last'] + '\n' + str(err.messages))
                continue

            #TODO Update database from CSV
            
            # Add new employee to session:
            db.session.add(new_employee)

        # Commit session to db:    
        db.session.commit()

        request.close()

        return '<h1>CSV Successfully Parsed</h1>'
    
    # Invalid filetype
    else:
        return '<h1>Invalid filetype</h1>'

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

    first = request.json['first'] 
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