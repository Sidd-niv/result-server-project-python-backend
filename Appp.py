import os
import re
import secrets
import matplotlib
from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from random import randint
from mail_pdff_den import *
import matplotlib.pyplot as plt
import rsa


# use matplotlib.use to generate multiple graphs
matplotlib.use('Agg')

# creating public-private key for encryption and decryption
publickey, privatekey = rsa.newkeys(512)

# Initialization
app = Flask(__name__)

# Initialization
db = SQLAlchemy(app)

# Configurations for application
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sidd@localhost/fyndacademy'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = secrets.token_hex(75)
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '*****************'
app.config['MAIL_PASSWORD'] = '*******'
app.config['MAIL_DEFAULT_SENDER'] = 'fyndproject05@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

# Initialization
mail = Mail()
mail.init_app(app)

# Creating a object of FPDF class
m_pdf = FPDF()


# ORM classes
class Studloginfo(db.Model):
    studId = db.Column(db.Integer(), primary_key=True)
    stud_name = db.Column(db.String(45), nullable=False)
    stud_email = db.Column(db.String(60), unique=True, nullable=False)

    # Methods to retrieve data from  sqlalchemy query
    def Js_stud(self):
        return {"stud_name": self.stud_name, "stud_email": self.stud_email}

    def js_stud_user_name(self):
        return {"stud_name": self.stud_name}

    def js_stud_user_email(self):
        return {"stud_email": self.stud_email}


# ORM class
class Studinfo(db.Model):
    stud_id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(60), unique=False, nullable=False)
    Gender = db.Column(db.String(45), unique=False, nullable=False)
    Sem = db.Column(db.Integer(), unique=False, nullable=False)
    Roll_no = db.Column(db.Integer(), unique=False, nullable=False)
    Div = db.Column(db.String(10), unique=False, nullable=False)
    Paper_1 = db.Column(db.String(45), unique=False, nullable=False)
    Paper_2 = db.Column(db.String(45), unique=False, nullable=False)
    Paper_3 = db.Column(db.String(45), unique=False, nullable=False)
    Paper_4 = db.Column(db.String(45), unique=False, nullable=False)
    Paper_5 = db.Column(db.String(45), unique=False, nullable=False)
    Overall_Percentage = db.Column(db.String(45), unique=False, nullable=False)
    Stud_Result = db.Column(db.String(45), unique=False, nullable=False)

    # Methods to retrieve data from  sqlalchemy query
    def js_re(self):
        return {"stud_id": self.stud_id, "Name": self.Name, "Gender": self.Gender,
                "Sem_1": self.Sem, "Roll_no": self.Roll_no,
                "Div": self.Div, "Paper_1": self.Paper_1,
                "Paper_2": self.Paper_2, "Paper_3": self.Paper_3,
                "Paper_4": self.Paper_4, "Paper_5": self.Paper_5,
                "Overall_Percentage": self.Overall_Percentage,
                "Stud_Result": self.Stud_Result}

    def js_st_id(self):
        return {"stud_if": self.stud_id}

    def js_name(self):
        return {"Name": self.Name}

    def js_p1(self):
        return {"Paper-1": self.Paper_1}

    def js_p2(self):
        return {"Paper-2": self.Paper_2}

    def js_p3(self):
        return {"Paper-3": self.Paper_3}

    def js_p4(self):
        return {"Paper-4": self.Paper_4}

    def js_p5(self):
        return {"Paper-5": self.Paper_5}


# ORM class
class Teacherlogin(db.Model):
    Te_id = db.Column(db.Integer(), primary_key=True)
    teacher_name = db.Column(db.String(60), nullable=False)
    teacher_email = db.Column(db.String(80), nullable=False)
    t_password = db.Column(db.String(60), nullable=False)

    # Methods to retrieve data from  sqlalchemy query
    def js_log(self):
        return {"id": self.Te_id, "teacher_name": self.teacher_name,
                "teacher_email": self.teacher_email,
                "t_password": self.t_password}

    def js_staff_id(self):
        return {"id": self.Te_id}

    def js_staff_name(self):
        return {"name": self.teacher_name}

    def js_staff_email(self):
        return {"email": self.teacher_email}

    def js_staff_pass(self):
        return {"pass": self.teacher_email}


# ORM class
class Admininfo(db.Model):
    admin_name = db.Column(db.String(60), primary_key=True)
    admin_email = db.Column(db.String(80), unique=True, nullable=False)
    admin_pass = db.Column(db.String(60), unique=True, nullable=False)

    # Methods to retrieve data from  sqlalchemy query
    def js_add(self):
        return {
            "AdminD": self.admin_name,
            "Email": self.admin_email,
            "Password": self.admin_pass
        }


# Home Page
@app.route("/")
def home():
    return render_template("oppstudshaff.html")


@app.route("/studloginpg")
def studloginpg():
    return render_template("studD/newstudentlog.html")


@app.route("/stafflogpg")
def stafflogpg():
    return render_template("staffD/newstafflo.html")


@app.route("/Adminlogpg")
def Adminlogpg():
    return render_template("staffD/Adminlog.html")


@app.route("/invalidotppg")
def invalidotppg():
    return render_template("studD/Otppchek.html")


# Function to generate random otp
def gen_otp():
    g_otp = "".join([str(randint(1000, 9999)) for _ in range(1)])
    return g_otp


# Phase-1
# Student login to verify user name and email-id from database
@app.route("/studlogin", methods=["GET", "POST"])
def studlogin():
    if request.method == "POST":
        studName = request.form.get("name")
        stdName01 = studName.strip()
        stdName1 = stdName01.split(" ")
        stdName2 = " ".join([i.capitalize() for i in stdName1])
        studEm = request.form.get("email")
        try:
            stud = Studloginfo.Js_stud(Studloginfo.query.filter_by(stud_name=stdName2).first())
        except AttributeError:
            flash("Invalid UserName or Email-ID")
            return redirect(url_for('studloginpg'))
        if stud["stud_name"] == stdName2 and stud["stud_email"] == studEm:
            otp_1 = gen_otp()
            msg = Message("OTP", recipients=[stud["stud_email"]])
            msg.body = otp_1
            mail.send(msg)
            en_otp = rsa.encrypt(otp_1.encode(), publickey)
            session['response'] = {"Name": stdName2, "email": studEm, "OTP": en_otp}
            return render_template("studD/Otppchek.html")
        else:
            flash("Invalid UserName or Email-ID")
            return redirect(url_for('studlogin'))
    else:
        return redirect(url_for("studlogin"))


# OTP verify and sending email from database
@app.route("/Otpstud", methods=["GET", "POST"])
def otppg():
    global otp_email, otp1, otp_name
    if 'response' in session:
        if request.method == "POST":
            studOTp = request.form.get("otp")
            otp1 = session['response']["OTP"]
            otp_name = session['response']["Name"]
            otp_email = session['response']["email"]
            de_otp = rsa.decrypt(otp1, privatekey).decode()
            if de_otp == studOTp:
                try:
                    res_email = Studinfo.js_re(Studinfo.query.filter_by(Name=otp_name).first())
                except AttributeError:
                    flash("Invalid UserName or Email-ID")
                    return redirect(url_for('studloginpg'))
                msg_li = [
                    f"Name: {res_email['Name']} |Roll No: {res_email['Roll_no']} |Div: {res_email['Div']} |Sem: {res_email['Sem_1']}",
                    f"Paper-1 Marks: {res_email['Paper_1']}",
                    f"Paper-2 Marks: {res_email['Paper_2']}",
                    f"Paper-3 Marks: {res_email['Paper_3']}",
                    f"Paper-4 Marks: {res_email['Paper_4']}",
                    f"Paper-5 Marks: {res_email['Paper_5']}",
                    f"Percentage: {res_email['Overall_Percentage']}",
                    f"---------------------------------------",
                    f"Result: {res_email['Stud_Result']}"
                ]
                pdf = PDF(orientation="P", format="A4")
                pdf.add_page()  # it will add a page
                pdf.set_line_width(0.0)
                pdf.line(5.0, 5.0, 205.0, 5.0)  # top one
                pdf.line(5.0, 292.0, 205.0, 292.0)  # bottom one
                pdf.line(5.0, 5.0, 5.0, 292.0)  # left one
                pdf.line(205.0, 5.0, 205.0, 292.0)  # right one
                pdf.set_font(family="times", size=16)
                for line in msg_li:
                    pdf.cell(0, 10, txt=line, ln=True)
                pdf.output('FYND-Result.pdf', 'F')
                msg = Message("FYND SEM-1 Result", recipients=[otp_email])
                msg.body = f"{res_email['Name']} your sem:{res_email['Sem_1']} result"
                with app.open_resource('FYND-Result.pdf') as fp:
                    msg.attach('FYND-result.pdf', "application/pdf", fp.read())
                mail.send(msg)
                if 'response' in session:
                    session.pop('response', None)
                if os.path.exists("FYND-Result.pdf"):
                    os.remove("FYND-Result.pdf")
                return render_template("studD/email_re.html")
            else:
                flash('Please enter a valid OTP')
                return redirect(url_for('invalidotppg'))
    else:
        flash("Enter username and email-id")
        return render_template("studD/newstudentlog.html")


# Phase-2
# Staff--> Teacher login by verifying user input from databse
@app.route("/stafflogin", methods=["GET", "POST"])
def stafflogin():
    if "user_id" in session:
        session.pop("user_id", None)
    if request.method == 'POST':
        staff_user_name = request.form.get("stafname").strip()
        staff_user_pass = request.form.get("pwds").strip()
        try:
            staff_info = Teacherlogin.js_log(Teacherlogin.query.filter_by(teacher_name=staff_user_name).first())
        except AttributeError:
            flash("Invalid UserName or Password")
            return redirect(url_for('stafflogpg'))
        if staff_info["teacher_name"] == staff_user_name and staff_info["t_password"] == staff_user_pass:
            session["user_id"] = staff_info["teacher_name"]
            return redirect(url_for("resultpg"))
        else:
            flash("Invalid Username or Password")
            return redirect(url_for('stafflogpg'))
    else:
        return render_template("newstafflog.html")


# Teacher dashboard page
@app.route("/resultpg")
def resultpg():
    if "user_id" in session:
        return render_template("staffD/reind.html")
    else:
        flash("Please login")
        return redirect("stafflogpg")


# Paper-1 graph based data retrieved from database
@app.route("/Paper_1")
def Paper_1():
    if "user_id" in session:
        name_data_set = [Studinfo.js_name(a)["Name"][0:3] for a in Studinfo.query.all()]
        paperp1_data_set = [Studinfo.js_p1(a)["Paper-1"][0:2] for a in Studinfo.query.all()]
        p1_dict = {}
        for a, b in zip(name_data_set, paperp1_data_set):
            p1_dict[a] = int(b)
        plt.bar(p1_dict.keys(), [(v / 80) * 100 for v in p1_dict.values()])
        plt.xlabel("Students")
        plt.ylabel("Paper-1 Marks in perecentage")
        plt.grid(axis='y')
        plt.savefig("static/paperplot1.png")

        return render_template("staffD/studp1plot.html",
                               msg="This graph shows the marks of paper_1 scored by students in form of precentage ",
                               url="static/paperplot1.png")
    else:
        flash("Please login")
        return redirect("stafflogpg")


# Paper-2 graph based data retrieved from database
@app.route("/Paper_2")
def Paper_2():
    if "user_id" in session:
        name_data_set = [Studinfo.js_name(a)["Name"][0:3] for a in Studinfo.query.all()]
        paperp2_data_set = [Studinfo.js_p2(a)["Paper-2"][0:2] for a in Studinfo.query.all()]
        p1_dict = {}
        for a, b in zip(name_data_set, paperp2_data_set):
            p1_dict[a] = int(b)
        plt.bar(p1_dict.keys(), [(v / 80) * 100 for v in p1_dict.values()])
        plt.xlabel("Students")
        plt.ylabel("Paper-2 Marks precentage")
        plt.grid(axis='y')
        plt.savefig("static/paperplot2.png")

        return render_template("staffD/studp2plot.html",
                               msg2="This graph shows the Marks of paper_2 scored by students in form of precentage",
                               url="static/paperplot2.png")
    else:
        flash("Please login")
        return redirect("stafflogpg")


# Paper-3 graph based data retrieved from database
@app.route("/Paper_3")
def Paper_3():
    if "user_id" in session:
        name_data_set = [Studinfo.js_name(a)["Name"][0:3] for a in Studinfo.query.all()]
        paperp3_data_set = [Studinfo.js_p3(a)["Paper-3"][0:2] for a in Studinfo.query.all()]
        p1_dict = {}
        for a, b in zip(name_data_set, paperp3_data_set):
            p1_dict[a] = int(b)
        plt.bar(p1_dict.keys(), [(v / 80) * 100 for v in p1_dict.values()])
        plt.xlabel("Students")
        plt.ylabel("Paper-3 Marks Percentage")
        plt.grid(axis='y')
        plt.savefig("static/paperplot3.png")

        return render_template("staffD/studp3plot.html",
                               msg3="This graph shows the marks of paper_3 scored by students in form of precentage",
                               url="static/paperplot3.png")
    else:
        flash("Please login")
        return redirect("stafflogpg")


# Paper-4 graph based data retrieved from database
@app.route("/Paper_4")
def Paper_4():
    if "user_id" in session:
        name_data_set = [Studinfo.js_name(a)["Name"][0:3] for a in Studinfo.query.all()]
        paperp4_data_set = [Studinfo.js_p5(a)["Paper-5"][0:2] for a in Studinfo.query.all()]
        p1_dict = {}
        for a, b in zip(name_data_set, paperp4_data_set):
            p1_dict[a] = int(b)
        plt.bar(p1_dict.keys(), [(v / 80) * 100 for v in p1_dict.values()])
        plt.xlabel("Students")
        plt.ylabel("Paper-4 Marks percentage")
        plt.grid(axis='y')
        plt.savefig("static/paperplot4.png")
        print(paperp4_data_set)

        return render_template("staffD/studp4plot.html",
                               msg4="This graph shows the marks of paper_4 scored by students in form of precentage",
                               url="static/paperplot4.png")
    else:
        flash("Please login")
        return redirect("stafflogpg")


# Paper-5 graph based data retrieved from database
@app.route("/Paper_5")
def Paper_5():
    if "user_id" in session:
        name_data_set = [Studinfo.js_name(a)["Name"][0:3] for a in Studinfo.query.all()]
        paperp5_data_set = [int(Studinfo.js_p5(a)["Paper-5"][0:2]) for a in Studinfo.query.all()]
        p1_dict = {}
        for a, b in zip(name_data_set, paperp5_data_set):
            p1_dict[a] = int(b)
        plt.bar(p1_dict.keys(), [(v / 80) * 100 for v in p1_dict.values()])
        plt.xlabel("Students")
        plt.ylabel("Paper-5 Marks percentage")
        plt.grid(axis='y')
        plt.savefig("static/paperplot5.png")

        return render_template("staffD/studp5plot.html",
                               msg5="This graph shows the marks of paper_5 scored by student in form of precentage",
                               url="static/paperplot5.png")
    else:
        flash("Please login")
        return redirect("stafflogpg")


# Staff logout using session
@app.route('/logout')
def stafflogout():
    if "user_id" in session:
        session.pop("user_id", None)
        # delete logic to clear file generated for teachers
        if os.path.exists("static/paperplot1.png"):
            os.remove("static/paperplot1.png")
        if os.path.exists("static/paperplot2.png"):
            os.remove("static/paperplot2.png")
        if os.path.exists("static/paperplot3.png"):
            os.remove('static/paperplot3.png')
        if os.path.exists("static/paperplot4.png"):
            os.remove('static/paperplot4.png')
        if os.path.exists("static/paperplot5.png"):
            os.remove('static/paperplot5.png')
    return render_template("staffD/newstafflo.html")


# Phase-3
# Admin login by verifying client login detail
@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    if "user_id2" in session:
        session.pop("user_id2", None)
    if request.method == 'POST':
        add_user_name = request.form.get("addname").strip()
        add_user_pass = request.form.get("addpwds").strip()
        try:
            admin_info = Admininfo.js_add(Admininfo.query.filter_by(admin_name=add_user_name).first())
        except AttributeError:
            flash("Invalid UserName or Password")
            return redirect(url_for('Adminlogpg'))
        if admin_info["AdminD"] == add_user_name and admin_info["Password"] == add_user_pass:
            session["user_id2"] = admin_info["AdminD"]
            return redirect(url_for('admindashpg'))
        else:
            flash("Invalid Username or Password")
            return redirect(url_for('Adminlogpg'))
    else:
        return render_template("staffD/Adminlog.html")


# Admin dashboard
@app.route("/admindashpg")
def admindashpg():
    if "user_id2" in session:
        return render_template("staffD/adminpro.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Adding new student result details
@app.route("/addstudinfoo", methods=['GET', 'POST'])
def addstudinfoo():
    if "user_id2" in session:
        if request.method == 'POST':
            stud_id_list = [Studinfo.js_st_id(a)['stud_if'] for a in Studinfo.query.all()]
            new_stud_id = len(stud_id_list) + 1
            new_stud_name = request.form.get('studname').strip()
            name_check = re.findall(r'[0-9]+', new_stud_name)
            name_check_list = []
            if name_check != name_check_list:
                msgname = 'please enter a student name valid input'
                return render_template("staffD/Adminstudinfoadd.html", msgname=msgname)
            new_stud_name1 = new_stud_name.split(" ")
            new_stud_name2 = " ".join([i.capitalize() for i in new_stud_name1])
            stud_name_check = [Studinfo.js_name(a)["Name"] for a in Studinfo.query.all()]
            if new_stud_name2 in stud_name_check:
                msgname = 'Student Name already exists'
                return render_template("staffD/Adminstudinfoadd.html", msgname=msgname)
            new_stud_gen = request.form.get('gen')
            new_stud_sem = request.form.get('sem')
            new_stud_roll = request.form.get('rollno').strip()
            new_stud_div = request.form.get('div')
            new_stud_p1 = request.form.get('p1').strip()
            try:
                if new_stud_p1[2] != "/":
                    msgp1 = 'please enter a valid input in paper-1'
                    return render_template("staffD/Adminstudinfoadd.html", msgp1=msgp1)
                if int(new_stud_p1[0:2]) > 80 or int(new_stud_p1[3::]) > 80:
                    msgp1 = 'please enter valid marks of paper-1 '
                    return render_template("staffD/Adminstudinfoadd.html", msgp1=msgp1)
            except IndexError:
                msgp1 = 'Invalid response'
                return render_template("staffD/Adminstudinfoadd.html", msgp1=msgp1)
            new_stud_p2 = request.form.get('p2').strip()
            try:
                if new_stud_p2[2] != "/":
                    msgp2 = 'please enter a valid input in paper-2'
                    return render_template("staffD/Adminstudinfoadd.html", msgp2=msgp2)
                if int(new_stud_p2[0:2]) > 80 or int(new_stud_p2[3::]) > 80:
                    msgp2 = 'please enter valid marks for paper-2'
                    return render_template("staffD/Adminstudinfoadd.html", msgp2=msgp2)
            except IndexError:
                msgp2 = 'Invalid response'
                return render_template("staffD/Adminstudinfoadd.html", msgp1=msgp2)
            new_stud_p3 = request.form.get('p3').strip()
            try:
                if new_stud_p3[2] != "/":
                    msgp3 = 'please enter a valid input in paper-3'
                    return render_template("staffD/Adminstudinfoadd.html", msgp3=msgp3)
                if int(new_stud_p3[0:2]) > 80 or int(new_stud_p3[3::]) > 80:
                    msgp3 = 'please enter valid marks for paper-3'
                    return render_template("staffD/Adminstudinfoadd.html", msgp3=msgp3)
            except IndexError:
                msgp3 = 'Invalid response'
                return render_template("staffD/Adminstudinfoadd.html", msgp3=msgp3)
            new_stud_p4 = request.form.get('p4').strip()
            try:
                if new_stud_p4[2] != "/":
                    msgp4 = 'please enter a valid input in paper-4'
                    return render_template("staffD/Adminstudinfoadd.html", msgp4=msgp4)
                if int(new_stud_p4[0:2]) > 80 or int(new_stud_p4[3::]) > 80:
                    msgp4 = 'please enter valid marks for paper-4'
                    return render_template("staffD/Adminstudinfoadd.html", msgp4=msgp4)
            except IndexError:
                msgp4 = 'Invalid response'
                return render_template("staffD/Adminstudinfoadd.html", msgp4=msgp4)
            new_stud_p5 = request.form.get('p5').strip()
            try:
                if new_stud_p5[2] != "/":
                    msgp5 = 'please enter a valid input in paper-5'
                    return render_template("staffD/Adminstudinfoadd.html", msgp5=msgp5)
                if int(new_stud_p5[0:2]) > 80 or int(new_stud_p5[3::]) > 80:
                    msgp5 = 'please enter valid marks'
                    return render_template("staffD/Adminstudinfoadd.html", msgp5=msgp5)
            except IndexError:
                msgp5 = 'Invalid response'
                return render_template("staffD/Adminstudinfoadd.html", msgp4=msgp5)
            try:
                stud_total = int(new_stud_p1[0:2]) + int(new_stud_p2[0:2]) + int(new_stud_p3[0:2]) + int(
                    new_stud_p4[0:2]) + int(new_stud_p5[0:2])
            except ValueError:
                msgerror = "Invalid marks"
                return render_template("staffD/Adminstudinfoadd.html", msgerror=msgerror)
            new_stud_percen1 = ((stud_total / 400) * 100)
            new_stud_percen = f"{new_stud_percen1}%"
            if new_stud_percen1 >= 32.00:
                new_stud_result = "Pass"
            else:
                new_stud_result = "Fail"
            old_stud_name = [Studinfo.js_name(a) for a in Studinfo.query.all()]
            if {"Name": new_stud_name2} in old_stud_name:
                flash(f"{new_stud_name2} data already exists")
                return render_template("staffD/Adminstudinfoadd.html")
            entry = Studinfo(stud_id=new_stud_id, Name=new_stud_name2,
                             Gender=new_stud_gen, Sem=new_stud_sem,
                             Roll_no=new_stud_roll, Div=new_stud_div,
                             Paper_1=new_stud_p1, Paper_2=new_stud_p2,
                             Paper_3=new_stud_p3, Paper_4=new_stud_p4,
                             Paper_5=new_stud_p5, Overall_Percentage=new_stud_percen,
                             Stud_Result=new_stud_result)
            db.session.add(entry)
            db.session.commit()
            stud_lo_id = [Studloginfo.js_stud_user_name(a)["stud_name"] for a in Studloginfo.query.all()]
            entry2 = Studloginfo(studId=len(stud_lo_id)+1, stud_name=new_stud_name2,
                                 stud_email=f"xyz{len(stud_lo_id) + 2}@gamil.com")
            db.session.add(entry2)
            db.session.commit()
            msgadd = "Student data added"
            return render_template("staffD/Adminstudinfoadd.html", msgadd=msgadd)
        return render_template("staffD/Adminstudinfoadd.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Student name updating function
@app.route("/updateinfo", methods=["GET", "POST"])
def updateinfo():
    if "user_id2" in session:
        if request.method == "POST":
            old_name = request.form.get("olname").strip()
            new_name = request.form.get("nename").strip()
            name_check = re.findall(r'[0-9]+', new_name)
            name_valid = []
            if name_valid != name_check:
                m1 = 'please enter a student name valid input'
                return render_template("staffD/studinfoupdate.html", msg2=m1)
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=old_name).first())
            except AttributeError:
                m2 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg3=m2)
            update_login_name = Studloginfo.query.filter_by(stud_name=old_name).first()
            update_login_name.stud_name = new_name
            update_name = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_name.Name = new_name
            db.session.commit()
            fl_msg = "Student name updated!!"
            return render_template("staffD/studinfoupdate.html", fl_msg=fl_msg)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Student paper-1 marks updating function
@app.route("/updateinfop1", methods=["GET", "POST"])
def updateinfop1():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p1name").strip()
            name_check = re.findall(r'[0-9]+', name)
            name_check_list = []
            if name_check != name_check_list:
                msg01 = 'please enter a student name valid input'
                return render_template("staffD/studinfoupdate.html", msg01=msg01)
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg02 = "Student Not found"
                return render_template("staffD/studinfoupdate.html", msg02=msg02)
            paper_01 = request.form.get("p1").strip()
            try:
                if paper_01[2] != "/":
                    msgp1er = 'please enter valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp1er=msgp1er)
                if int(paper_01[0:2]) > 80 or int(paper_01[3::]) > 80:
                    msgp1er = 'please enter  valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp1er=msgp1er)
            except IndexError:
                msgp1er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp1er=msgp1er)
            try:
                stud_total = int(paper_01[0:2]) + int(check_data["Paper_2"][0:2]) + int(
                    check_data["Paper_3"][0:2]) + int(check_data["Paper_4"][0:2]) \
                             + int(check_data['Paper_5'][0:2])
            except ValueError:
                msgp1er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp1er=msgp1er)
            new_stud_percen = ((stud_total / 400) * 100)
            update_p1 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p1.Paper_1 = paper_01
            update_p1.Overall_Percentage = f"{new_stud_percen}%"
            if int(new_stud_percen) >= 32:
                update_p1.Stud_Result = "Pass"
            else:
                update_p1.Stud_Result = "Fail"
            db.session.commit()
            msg04 = "Paper-1 marks updated for previous student"
            return render_template("staffD/studinfoupdate.html", msg04=msg04)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Student paper-2 marks updating function
@app.route("/updateinfop2", methods=["GET", "POST"])
def updateinfop2():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p2name").strip()
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg21 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg21=msg21)
            paper_02 = request.form.get("p2").strip()
            try:
                if paper_02[2] != "/":
                    msgp2er = 'please enter valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp2er=msgp2er)
                if int(paper_02[0:2]) > 80 or int(paper_02[3::]) > 80:
                    msgp2er = 'please enter valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp2er=msgp2er)
            except IndexError:
                msgp2er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp2er=msgp2er)
            try:
                stud_total = int(paper_02[0:2]) + int(check_data["Paper_1"][0:2]) + int(
                    check_data["Paper_3"][0:2]) + int(check_data["Paper_4"][0:2]) \
                             + int(check_data['Paper_5'][0:2])
            except ValueError:
                msgp2er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp2er=msgp2er)
            new_stud_percen = ((stud_total / 400) * 100)
            update_p2 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p2.Paper_2 = paper_02
            update_p2.Overall_Percentage = f"{new_stud_percen}%"
            if int(new_stud_percen) >= 32:
                update_p2.Stud_Result = "Pass"
            else:
                update_p2.Stud_Result = "Fail"
            db.session.commit()
            msg23 = "Student Paper-2 marks updated!"
            return render_template("staffD/studinfoupdate.html", msg23=msg23)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Student paper-2 marks updating function
@app.route("/updateinfop3", methods=["GET", "POST"])
def updateinfop3():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p3name").strip()
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg31 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg31=msg31)
            paper_03 = request.form.get("p3").strip()
            try:
                if paper_03[2] != "/":
                    msgp3er = 'please enter valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp3er=msgp3er)
                if int(paper_03[0:2]) > 80 or int(paper_03[3::]) > 80:
                    msgp3er = 'please enter  valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp3er=msgp3er)
            except IndexError:
                msgp3er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp3er=msgp3er)
            try:
                stud_total = int(paper_03[0:2]) + int(check_data["Paper_1"][0:2]) + int(
                    check_data["Paper_2"][0:2]) + int(check_data["Paper_4"][0:2]) \
                             + int(check_data['Paper_5'][0:2])
            except ValueError:
                msgp3er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp3er=msgp3er)
            new_stud_percen = ((stud_total / 400) * 100)
            update_p3 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p3.Paper_3 = paper_03
            update_p3.Overall_Percentage = f"{new_stud_percen}%"
            if int(new_stud_percen) >= 32:
                update_p3.Stud_Result = "Pass"
            else:
                update_p3.Stud_Result = "Fail"
            db.session.commit()
            msg33 = "Previous student marks updated!!"
            return render_template("staffD/studinfoupdate.html", msg33=msg33)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Student paper-4 marks updating function
@app.route("/updateinfop4", methods=["GET", "POST"])
def updateinfop4():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p4name").strip()
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg41 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg41=msg41)
            paper_04 = request.form.get("p4").strip()
            try:
                if paper_04[2] != "/":
                    msgp4er = 'please enter valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp4er=msgp4er)
                if int(paper_04[0:2]) > 80 or int(paper_04[3::]) > 80:
                    msgp4er = 'please enter  valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp4er=msgp4er)
            except IndexError:
                msgp4er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp4er=msgp4er)
            try:
                stud_total = int(paper_04[0:2]) + int(check_data["Paper_1"][0:2]) + int(
                    check_data["Paper_2"][0:2]) + int(check_data["Paper_3"][0:2]) \
                             + int(check_data['Paper_5'][0:2])
            except ValueError:
                msgp4er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp4er=msgp4er)
            new_stud_percen = ((stud_total / 400) * 100)
            update_p3 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p3.Paper_4 = paper_04
            update_p3.Overall_Percentage = f"{new_stud_percen}%"
            if int(new_stud_percen) >= 32:
                update_p3.Stud_Result = "Pass"
            else:
                update_p3.Stud_Result = "Fail"
            db.session.commit()
            msg43 = "Previous student marks updated!!"
            return render_template("staffD/studinfoupdate.html", msg43=msg43)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Student paper-5 marks updating function
@app.route("/updateinfop5", methods=["GET", "POST"])
def updateinfop5():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p5name").strip()
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg51 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg51=msg51)
            paper_05 = request.form.get("p5").strip()
            try:
                if paper_05[2] != "/":
                    msgp5er = 'please enter valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp5er=msgp5er)
                if int(paper_05[0:2]) > 80 or int(paper_05[3::]) > 80:
                    msgp5er = 'please enter  valid marks'
                    return render_template("staffD/studinfoupdate.html", msgp5er=msgp5er)
            except IndexError:
                msgp5er = 'Invalid response'
                return render_template("staffD/studinfoupdate.html", msgp5er=msgp5er)
            try:
                stud_total = int(paper_05[0:2]) + int(check_data["Paper_1"][0:2]) + int(
                    check_data["Paper_2"][0:2]) + int(check_data["Paper_3"][0:2]) \
                             + int(check_data['Paper_4'][0:2])
            except ValueError:
                msgp5er = 'please enter  valid marks'
                return render_template("staffD/studinfoupdate.html", msgp5er=msgp5er)
            new_stud_percen = ((stud_total / 400) * 100)
            update_p5 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p5.Paper_5 = paper_05
            update_p5.Overall_Percentage = f"{new_stud_percen}%"
            if int(new_stud_percen) >= 32:
                update_p5.Stud_Result = "Pass"
            else:
                update_p5.Stud_Result = "Fail"
            db.session.commit()
            msg54 = "Previous student marks updated!!"
            return render_template("staffD/studinfoupdate.html", msg54=msg54)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Student data removal from database
@app.route('/studdelpg', methods=["GET", "POST"])
def studdelpg():
    if "user_id2" in session:
        if request.method == "POST":
            del_info = request.form.get("studnamed").strip()
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=del_info).first())
            except AttributeError:
                flash("Student data not found")
                return redirect("studdelpg")
            del_stu_in = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            db.session.delete(del_stu_in)
            db.session.commit()
            stud_name_list = [Studinfo.js_name(a)["Name"] for a in Studinfo.query.all()]
            j = 0
            for i in stud_name_list:
                j += 1
                update_check_data = Studinfo.query.filter_by(Name=i).first()
                update_check_data.stud_id = j
                db.session.commit()
            msg_de = "Student data deleted"
            return render_template("staffD/admindelinfo.html", msg_de=msg_de)
        return render_template("staffD/admindelinfo.html")
    else:
        flash("Admin login required")
    return render_template("staffD/Adminlog.html")


# Read function to view student data from database
@app.route('/viewstud', methods=["GET", "POST"])
def viewstud():
    if "user_id2" in session:
        if request.method == "POST":
            stud_name_v = request.form.get("view").strip()
            name_check = re.findall(r'[0-9]+', stud_name_v)
            name_valid = []
            if name_valid != name_check:
                vm = 'please enter a student name valid input'
                return render_template("staffD/viewstud.html", msg1=vm)
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=stud_name_v).first())
            except AttributeError:
                flash("Student doesn't exist ")
                return redirect("viewstud")
            show_stud = Studinfo.js_re(Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first())
            Name = show_stud["Name"]
            if show_stud["Gender"] == "1":
                gen = "Male"
            else:
                gen = "Female"
            sem = show_stud["Sem_1"]
            div = show_stud['Div']
            Paper1 = show_stud["Paper_1"]
            Paper2 = show_stud["Paper_2"]
            Paper3 = show_stud["Paper_3"]
            Paper4 = show_stud["Paper_4"]
            Paper5 = show_stud["Paper_5"]
            per = show_stud["Overall_Percentage"]
            ress = show_stud["Stud_Result"]
            return render_template("staffD/studviewtable.html",
                                   Name=Name, gen=gen, sem=sem,
                                   div=div, Paper_1=Paper1,
                                   Paper_2=Paper2, Paper_3=Paper3,
                                   Paper_4=Paper4, Paper_5=Paper5,
                                   per=per, ress=ress)
        return render_template("staffD/viewstud.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Adding new staff user name and password
@app.route("/staffidadd", methods=["GET", "POST"])
def staffidadd():
    if "user_id2" in session:
        if request.method == "POST":
            new_staff_name = request.form.get("sfid").strip()
            new_staff_email = request.form.get("sfemail").strip()
            new_staff_pass = request.form.get("pwds").strip()
            name_check = re.findall(r'[0-9]+', new_staff_name)
            name_check_list = []
            if name_check != name_check_list:
                return render_template("staffD/staff_and_student_info_update_add.html",
                                       namsg="Please enter valid user name")
            staff_name_check_list = [Teacherlogin.js_staff_name(a)["name"] for a in Teacherlogin.query.all()]
            print(staff_name_check_list)
            if new_staff_name in staff_name_check_list:
                return render_template("staffD/staff_and_student_info_update_add.html",
                                       namsg="Staff User name already exists")
            staff_email_check_list = [Teacherlogin.js_staff_email(a)["email"] for a in Teacherlogin.query.all()]
            if new_staff_email in staff_email_check_list:
                return render_template("staffD/staff_and_student_info_update_add.html", namsg2="Staff email_id  exists")
            staff_id_list = [Teacherlogin.js_staff_id(a) for a in Teacherlogin.query.all()]
            new_id = len(staff_id_list) + 1
            entry = Teacherlogin(Te_id=new_id, teacher_name=new_staff_name,
                                 teacher_email=new_staff_email, t_password=new_staff_pass)
            db.session.add(entry)
            db.session.commit()
            return render_template("staffD/staff_and_student_info_update_add.html", msgdone="User created")
        return render_template("staffD/staff_and_student_info_update_add.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Updating staff user name and password
@app.route("/upstaffid", methods=["GET", "POST"])
def upstaffid():
    if "user_id2" in session:
        if request.method == "POST":
            staff_up_name = request.form.get("upstid").strip()
            try:
                check_dta = Teacherlogin.js_log(Teacherlogin.query.filter_by(teacher_name=staff_up_name).first())
            except AttributeError:
                return render_template("staffD/staff_and_student_info_update_add.html", upmsg="staff data not found")
            update_email = request.form.get("stemail").strip()
            update_pass = request.form.get("pwds").strip()
            check_email_null_list = [a for a in update_email]
            check_pass_null_list = [a for a in update_pass]
            null_list = []
            if check_email_null_list != null_list and check_pass_null_list != null_list:
                update_allemail_f = Teacherlogin.query.filter_by(Te_id=check_dta["id"]).first()
                update_allemail_f.teacher_email = update_email
                update_allemail_f.t_password = update_pass
                return render_template("staffD/staff_and_student_info_update_add.html",
                                       upmsg3="email and password updated")
            if check_pass_null_list == null_list:
                update_email_f = Teacherlogin.query.filter_by(Te_id=check_dta["id"]).first()
                update_email_f.teacher_email = update_email
                return render_template("staffD/staff_and_student_info_update_add.html", upmsg1="email updated")
            if check_email_null_list == null_list:
                update_password = Teacherlogin.query.filter_by(Te_id=check_dta["id"]).first()
                update_password.t_password = update_pass
                return render_template("staffD/staff_and_student_info_update_add.html", upmsg2="Password update")
        return render_template("staffD/staff_and_student_info_update_add.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Updating student login user name and email-id
@app.route("/stuidadd", methods=["GET", "POST"])
def stuidadd():
    if "user_id2" in session:
        if request.method == "POST":
            new_user_stud = request.form.get("stid").strip()
            new_user_stud_email = request.form.get("stuemail").strip()
            data_check_name = [Studloginfo.js_stud_user_name(a)["stud_name"] for a in Studloginfo.query.all()]
            print(data_check_name)
            data_check_email = [Studloginfo.js_stud_user_email(a)["stud_email"] for a in Studloginfo.query.all()]
            print(data_check_email)
            if new_user_stud in data_check_name:
                return render_template("staffD/staff_and_student_info_update_add.html", msguser="User already exists")
            if new_user_stud_email in data_check_email:
                return render_template("staffD/staff_and_student_info_update_add.html",
                                       msgemail="User email already exists")
            entry = Studloginfo(studId=len(data_check_name) + 1,
                                stud_name=new_user_stud,
                                stud_email=new_user_stud_email)

            db.session.add(entry)
            db.session.commit()
            return render_template("staffD/staff_and_student_info_update_add.html", stad="student login info added")
        return render_template("staffD/staff_and_student_info_update_add.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Reading all student login info using jsonify
@app.route('/showallstudlog', methods=['GET'])
def allstudlog():
    if "user_id2" in session:
        all_studlog = [Studloginfo.Js_stud(data_items) for data_items in Studloginfo.query.all()]
        return jsonify(all_studlog)
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


# Logout function using session
@app.route('/adminlogout')
def adminlogout():
    if "user_id2" in session:
        session.pop("user_id2", None)
    return render_template("staffD/Adminlog.html")


if __name__ == "__main__":
    app.run(debug=True)
