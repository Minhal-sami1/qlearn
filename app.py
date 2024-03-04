from flask import Flask, render_template, redirect, url_for, request, session, send_file
from models import db, Teacher, Student, Course
from datetime import datetime
from sqlalchemy import func
from functools import wraps
from flask_wtf import CSRFProtect 
import requests
import pandas as pd
from datetime import datetime
import gunicorn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key_change_it_minhal'


def convertCurrency(cFrom, cTo, cAmount):
	response = requests.get(f"https://open.er-api.com/v6/latest/{cFrom}").json()
	convert_rate = response["rates"][cTo]
	return round(convert_rate*cAmount, 2)
currency = {
    "USD": "United States Dollar",
    "AED": "United Arab Emirates Dirham",
    "AFN": "Afghan Afghani",
    "ALL": "Albanian Lek",
    "AMD": "Armenian Dram",
    "ANG": "Netherlands Antillean Guilder",
    "AOA": "Angolan Kwanza",
    "ARS": "Argentine Peso",
    "AUD": "Australian Dollar",
    "AWG": "Aruban Florin",
    "AZN": "Azerbaijani Manat",
    "BAM": "Bosnia and Herzegovina Convertible Mark",
    "BBD": "Barbadian Dollar",
    "BDT": "Bangladeshi Taka",
    "BGN": "Bulgarian Lev",
    "BHD": "Bahraini Dinar",
    "BIF": "Burundian Franc",
    "BMD": "Bermudian Dollar",
    "BND": "Brunei Dollar",
    "BOB": "Bolivian Boliviano",
    "BRL": "Brazilian Real",
    "BSD": "Bahamian Dollar",
    "BTN": "Bhutanese Ngultrum",
    "BWP": "Botswana Pula",
    "BYN": "Belarusian Ruble",
    "BZD": "Belize Dollar",
    "CAD": "Canadian Dollar",
    "CDF": "Congolese Franc",
    "CHF": "Swiss Franc",
    "CLP": "Chilean Peso",
    "CNY": "Chinese Yuan",
    "COP": "Colombian Peso",
    "CRC": "Costa Rican Colón",
    "CUP": "Cuban Peso",
    "CVE": "Cape Verdean Escudo",
    "CZK": "Czech Republic Koruna",
    "DJF": "Djiboutian Franc",
    "DKK": "Danish Krone",
    "DOP": "Dominican Peso",
    "DZD": "Algerian Dinar",
    "EGP": "Egyptian Pound",
    "ERN": "Eritrean Nakfa",
    "ETB": "Ethiopian Birr",
    "EUR": "Euro",
    "FJD": "Fijian Dollar",
    "FKP": "Falkland Islands Pound",
    "FOK": "Faroese Króna",
    "GBP": "British Pound Sterling",
    "GEL": "Georgian Lari",
    "GGP": "Guernsey Pound",
    "GHS": "Ghanaian Cedi",
    "GIP": "Gibraltar Pound",
    "GMD": "Gambian Dalasi",
    "GNF": "Guinean Franc",
    "GTQ": "Guatemalan Quetzal",
    "GYD": "Guyanaese Dollar",
    "HKD": "Hong Kong Dollar",
    "HNL": "Honduran Lempira",
    "HRK": "Croatian Kuna",
    "HTG": "Haitian Gourde",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "IMP": "Isle of Man Pound",
    "INR": "Indian Rupee",
    "IQD": "Iraqi Dinar",
    "IRR": "Iranian Rial",
    "ISK": "Icelandic Króna",
    "JEP": "Jersey Pound",
    "JMD": "Jamaican Dollar",
    "JOD": "Jordanian Dinar",
    "JPY": "Japanese Yen",
    "KES": "Kenyan Shilling",
    "KGS": "Kyrgyzstani Som",
    "KHR": "Cambodian Riel",
    "KID": "Kiribati Dollar",
    "KMF": "Comorian Franc",
    "KRW": "South Korean Won",
    "KWD": "Kuwaiti Dinar",
    "KYD": "Cayman Islands Dollar",
    "KZT": "Kazakhstani Tenge",
    "LAK": "Laotian Kip",
    "LBP": "Lebanese Pound",
    "LKR": "Sri Lankan Rupee",
    "LRD": "Liberian Dollar",
    "LSL": "Lesotho Loti",
    "LYD": "Libyan Dinar",
    "MAD": "Moroccan Dirham",
    "MDL": "Moldovan Leu",
    "MGA": "Malagasy Ariary",
    "MKD": "Macedonian Denar",
    "MMK": "Myanmar Kyat",
    "MNT": "Mongolian Tugrik",
    "MOP": "Macanese Pataca",
    "MRU": "Mauritanian Ouguiya",
    "MUR": "Mauritian Rupee",
    "MVR": "Maldivian Rufiyaa",
    "MWK": "Malawian Kwacha",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "MZN": "Mozambican Metical",
    "NAD": "Namibian Dollar",
    "NGN": "Nigerian Naira",
    "NIO": "Nicaraguan Córdoba",
    "NOK": "Norwegian Krone",
    "NPR": "Nepalese Rupee",
    "NZD": "New Zealand Dollar",
    "OMR": "Omani Rial",
    "PAB": "Panamanian Balboa",
    "PEN": "Peruvian Nuevo Sol",
    "PGK": "Papua New Guinean Kina",
    "PHP": "Philippine Peso",
    "PKR": "Pakistani Rupee",
    "PLN": "Polish Złoty",
    "PYG": "Paraguayan Guarani",
    "QAR": "Qatari Rial",
    "RON": "Romanian Leu",
    "RSD": "Serbian Dinar",
    "RUB": "Russian Ruble",
    "RWF": "Rwandan Franc",
    "SAR": "Saudi Riyal",
    "SBD": "Solomon Islands Dollar",
    "SCR": "Seychellois Rupee",
    "SDG": "Sudanese Pound",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "SHP": "Saint Helena Pound",
    "SLE": "Sierra Leonean Leone",
    "SLL": "Sierra Leonean Leone",
    "SOS": "Somali Shilling",
    "SRD": "Surinamese Dollar",
    }




db.init_app(app)
csrf = CSRFProtect(app) 

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            if session['logged_in']:
                return view_func(*args, **kwargs)
            else:
                return redirect(url_for('index'))
        except KeyError:
            return redirect(url_for('index'))
    return wrapper

def select_valid_table(id):
    tables = (Teacher.query.filter_by(id=id), Student.query.filter_by(id=id), Course.query.filter_by(id=id))
    for table in tables:
        if table.count() > 0:
            return (table.first(), tables.index(table))

## Common Routes

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=["GET", "POST"])
def index():
    if (request.method == "POST" and request.form['password'] == '123456789'):
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.get('/zakat')
@login_required
def zakat():
    return render_template('zakat.html')

# create a function to convert currency


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', tobj=Teacher, sobj=Student, cobj=Course)

@app.route('/accounting')
@login_required
def accounting():
    ## All Receivables from students with PKR currency
    pkr_total_revenue = Student.query.filter(Student.currency == "PKR").all()
    pkr_total_revenue = sum([int(student.fee) for student in pkr_total_revenue])
    ## Received from students with PKR currency
    pkr_total_revenue_received = Student.query.filter(Student.currency == "PKR", Student.isFeePaid==True).all()
    pkr_total_revenue_received = sum([int(student.fee) for student in pkr_total_revenue_received])
    ## All Receivables from students with non PKR currency
    non_pkr_total_revenue = Student.query.filter(Student.currency != "PKR").all()
    non_pkr_total_revenue = sum([int(convertCurrency(student.currency, "PKR", int(student.fee))) for student in non_pkr_total_revenue])
    ## Received from students with non PKR currency
    non_pkr_total_revenue_received = Student.query.filter(Student.currency != "PKR", Student.isFeePaid==True).all()
    non_pkr_total_revenue_received = sum([int(convertCurrency(student.currency, "PKR", int(student.fee))) for student in non_pkr_total_revenue_received])


    ## Cost of revenue
    total_cost_of_revenue = Teacher.query.all()
    total_cost_of_revenue = sum([int(teacher.salary) for teacher in total_cost_of_revenue])

    ## Cost of revenue paid
    total_cost_of_revenue_paid = Teacher.query.filter_by(isSalaryPaid=True).all()
    total_cost_of_revenue_paid = sum([int(teacher.salary) for teacher in total_cost_of_revenue_paid])

    projected_gross_profit = (pkr_total_revenue + non_pkr_total_revenue) - total_cost_of_revenue
    current_gross_profit = (pkr_total_revenue_received + non_pkr_total_revenue_received) - total_cost_of_revenue_paid

    return render_template('accounts.html', pkr_total_revenue=pkr_total_revenue, pkr_total_revenue_received=pkr_total_revenue_received, non_pkr_total_revenue=non_pkr_total_revenue,non_pkr_total_revenue_received=non_pkr_total_revenue_received,total_cost_of_revenue=total_cost_of_revenue,total_cost_of_revenue_paid=total_cost_of_revenue_paid,projected_gross_profit=projected_gross_profit,current_gross_profit=current_gross_profit)







@app.get('/view/<id>')
@login_required
def view(id):
    table, table_index = select_valid_table(id)
    return render_template('view.html', table=table, table_index=table_index, sobj=Student, cobj=Course, tobj=Teacher, currency=currency)

@app.get('/edit/<id>')
@login_required
def edit(id):
    table, table_index = select_valid_table(id)
    quran_courses_choices = ['Nazra', 'Hifz', 'Tajweed', 'Tafseer', 'Ta\'wil', 'Hadiths', 'Fiqh', 'Seerah', 'Quran Arabic (with grammar)', 'Quran Arabic (without grammar)', 'Methods of Worship', 'Islam Basics']
    teachers = Teacher.query.order_by(Teacher.name).all()
    platforms = ["WhatsApp", "Instagram", "Facebook", "Twitter/X", "Zoom", "Google Meet", "Skype", "Gmeet", "Discord", "Microsoft Teams"]
    
    if table_index == 2:
        quran_courses_choices.remove(table.course_type)
    elif table_index == 1:
        platforms.remove(table.platform)
    return render_template('edit.html', table=table, table_index=table_index, sobj=Student, cobj=Course, tobj=Teacher, quran_courses_choices=quran_courses_choices, teachers=teachers, platforms=platforms, currency=currency)

@app.post('/edit/<id>')
@login_required
def edit_post(id):
    table, table_index = select_valid_table(id)
    ## Teacher Details
    if table_index == 0:
        table.name = request.form['name']
        table.contact = request.form['contact']
        table.contact_nickname = request.form['contact-nickname']
        table.country = request.form['country']
        table.city = request.form['city']
        table.address = request.form['address']
        table.qualification = request.form['qualifications']
        table.cnic_number = request.form['cnic']
        table.join_date = datetime.strptime(request.form['date-joined'], '%Y-%m-%d')
        table.salary = request.form['salary']
        table.account_of_payment = request.form['payment']
        table.languages = request.form['languages']
        db.session.commit()
    ## Student Details
    elif table_index == 1:

        table.name = request.form['name']
        table.contact = request.form['contact']
        table.country = request.form['country']
        table.city = request.form['city']
        table.address = request.form['address']
        table.payment_details = request.form['payment']
        table.birth_date = datetime.strptime(request.form['date-born'], '%Y-%m-%d')
        table.join_date = datetime.strptime(request.form['date-joined'], '%Y-%m-%d')
        table.course_id = request.form['course']
        table.fee = request.form['fee']
        table.platform = request.form['platform']
        table.contact_nickname = request.form['contact-nickname']
        table.languages = request.form['languages']
        table.timing = request.form['timing']
        table.currency = request.form['currency']
        db.session.commit()
    ## Course Details
    elif table_index == 2:
        table.name = request.form['title']
        table.details = request.form['details']
        table.teacher_id = request.form['teacher']
        table.course_type = request.form['class-type']
        db.session.commit()
    return redirect(url_for('edit', id=id))

## Teacher Routes

@app.route('/teachers')
@login_required
def all_teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@app.get('/teachers/add')
@login_required
def add_new_teacher():
    return render_template('add.html', table_index=0)

@app.post('/teachers/add')
@login_required
def add_new_teacher_post():
    new_teacher = Teacher(
        name=request.form['name'],
        contact_nickname=request.form['contact-nickname'],
        contact=request.form['contact'],
        country=request.form['country'],
        city=request.form['city'],
        address=request.form['address'],
        qualification=request.form['qualifications'],
        cnic_number=request.form['cnic'],
        join_date=datetime.strptime(request.form['date-joined'], '%Y-%m-%d'),
        salary=request.form['salary'],
        account_of_payment=request.form['payment'],
        languages=request.form['languages'],
    )
    db.session.add(new_teacher)
    db.session.commit()
    print("new teacher added")
    return redirect(url_for('all_teachers'))

@app.get("/toggle_salary/<teacher_id>")
@login_required
def mark_salary_as_paid(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    teacher.isSalaryPaid = not teacher.isSalaryPaid
    db.session.commit()
    return redirect(url_for('all_teachers'))


## Student Routes

@app.get('/students')
@login_required
def all_students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.get('/students/add')
@login_required
def all_new_students():
    platforms = ["WhatsApp", "Instagram", "Facebook", "Twitter/X", "Zoom", "Google Meet", "Skype", "Gmeet", "Discord", "Microsoft Teams"]
    classes = Course.query.order_by(Course.name).all()
    return render_template('add.html', table_index=1, classes=classes, platforms=platforms, currency=currency)

@app.post('/students/add')
@login_required
def add_student_post():
    new_student = Student(
        name=request.form['name'],
        contact=request.form['contact'],
        country=request.form['country'],
        city=request.form['city'],
        address=request.form['address'],
        payment_details=request.form['payment'],
        birth_date=datetime.strptime(request.form['date-born'], '%Y-%m-%d'),
        join_date=datetime.strptime(request.form['date-joined'], '%Y-%m-%d'),
        fee=request.form['fee'],
        platform=request.form['platform'],
        course_id=request.form['class'],
        contact_nickname=request.form['contact-nickname'],
        languages=request.form['languages'],
        timing=request.form['timing'],
        currency=request.form['currency'],
    )
    db.session.add(new_student)
    db.session.commit()
    print("new student added")
    return redirect(url_for('all_students'))

    student = Student.query.get_or_404(student_id)
    student.name = request.form['name']
    student.contact = request.form['contact']
    student.country = request.form['country']
    student.city = request.form['city']
    student.address = request.form['address']
    student.payment_details = request.form['payment']
    student.birth_date = datetime.strptime(request.form['birth-date'], '%Y-%m-%d')
    student.join_date = datetime.strptime(request.form['join-date'], '%Y-%m-%d')
    student.course_id = request.form['course']
    # student.account_of_payment = request.form['payment']
    db.session.commit()
    return redirect(url_for('edit_student', student_id=student.id))

@app.get('/toggle_fee/<student_id>')
@login_required
def fee_payment(student_id):
    student = Student.query.get_or_404(student_id)
    student.isFeePaid = not student.isFeePaid
    db.session.commit()
    return redirect(url_for('all_students'))

# Classes Routes

@app.get('/classes')
@login_required
def all_classes():
    courses = Course.query.order_by(Course.name).all()
    return render_template('classes.html', classes=courses, teacher_obj=Teacher, student_obj=Student)

@app.get('/classes/add')
@login_required
def add_classes():
    teachers = Teacher.query.order_by(Teacher.name).all()
    quran_courses_choices = ['Nazra', 'Hifz', 'Tajweed', 'Tafseer', 'Ta\'wil', 'Hadiths', 'Fiqh', 'Seerah', 'Quran Arabic (with grammar)', 'Quran Arabic (without grammar)', 'Methods of Worship', 'Islam Basics']
    return render_template('add.html', table_index=2, teachers=teachers, quran_courses_choices=quran_courses_choices)

@app.post('/classes/add')
@login_required
def add_classes_post():
    new_course = Course(
        name=request.form['title'],
        details=request.form['details'],
        teacher_id=request.form['teacher'],
        course_type=request.form['class-type'],
    )
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('all_classes'))


@app.get('/currency')
def exchange():
    return render_template('exchange.html', currency=currency)


@app.post('/currency')
def exchange_post():
    cFrom = request.form['currencyFrom']
    cTo = request.form['currencyTo']
    cAmount = request.form['amount']
    result = f"{convertCurrency(cFrom, cTo, float(cAmount)):,}"
    return render_template('exchange.html', result=result, currencyF=cFrom, currencyT=cTo, cAmount=cAmount, exchanged=True, currency=currency)

@app.get('/options')
def options():
    return render_template('options.html')

@app.get('/options/excel')
def options_excel():
    time = datetime.now().strftime("%Y-%m-%d")
    filename = f"./static/Data___{time}.xlsx"
    students = Student.query.all()
    teachers = Teacher.query.all()
    classes = Course.query.all()
    student_df = pd.DataFrame([student.__dict__ for student in students])
    teacher_df = pd.DataFrame([teacher.__dict__ for teacher in teachers])
    classes_df = pd.DataFrame([clas.__dict__ for clas in classes])
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        student_df.to_excel(writer, sheet_name='Students', index=False)
        teacher_df.to_excel(writer, sheet_name='Teachers', index=False)
        classes_df.to_excel(writer, sheet_name='Classes', index=False)
    return send_file(filename, as_attachment=True)


@app.get('/options/reset')
def options_reset():
    students = Student.query.all()
    teachers = Teacher.query.all()
    for student in students:
        student.isFeePaid = False
    for teacher in teachers:
        teacher.isSalaryPaid = False
    db.session.commit()
    return redirect(url_for('options'))




@app.get('/options/excel/un')
def options_excel_un():
    time = datetime.now().strftime("%Y-%m-%d")
    filename = f"./static/Accrued___{time}.xlsx"
    students = Student.query.filter_by(isFeePaid=False).all()
    teachers = Teacher.query.filter_by(isSalaryPaid=False).all()
    student_df = pd.DataFrame([student.__dict__ for student in students])
    teacher_df = pd.DataFrame([teacher.__dict__ for teacher in teachers])
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        student_df.to_excel(writer, sheet_name='Students', index=False)
        teacher_df.to_excel(writer, sheet_name='Teachers', index=False)

    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)