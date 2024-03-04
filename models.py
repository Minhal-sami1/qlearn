from flask_sqlalchemy import SQLAlchemy
import uuid
db = SQLAlchemy()

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    contact_nickname = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(800), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    cnic_number = db.Column(db.String(100), nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    account_of_payment = db.Column(db.String(1100), nullable=False)
    isSalaryPaid = db.Column(db.Boolean, default=False, nullable=False)
    languages = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f'<Teacher {self.name}>'
    

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    contact_nickname = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(800), nullable=False)
    payment_details = db.Column(db.String(900), nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    fee= db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    isFeePaid = db.Column(db.Boolean, default=False, nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    languages = db.Column(db.String(100), nullable=False)
    timing = db.Column(db.String(500), nullable=False)
    currency = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Student {self.name}>'
    

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(1000), nullable=False)
    course_type = db.Column(db.String(1000), nullable=False)
    teacher_id = db.Column(db.String(36), db.ForeignKey('teachers.id'), nullable=False)
    
    def __repr__(self):
        return f'<Course {self.name}>'