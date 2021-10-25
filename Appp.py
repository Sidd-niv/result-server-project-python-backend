import secrets
import os
import re
import io
from flask import Flask, render_template, request, session, flash, redirect, url_for, Response, send_file
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from random import randint
from mail_pdff_den import *
from matplotlib.ticker import PercentFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as figureCanvas
import matplotlib.pyplot as plt
import rsa

publickey, privatekey = rsa.newkeys(512)

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sidd@localhost/fyndacademy'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = secrets.token_hex(75)
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'fyndproject05@gmail.com'
app.config['MAIL_PASSWORD'] = 'Fyndpro@05'
app.config['MAIL_DEFAULT_SENDER'] = 'fyndproject05@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail()
mail.init_app(app)
m_pdf = FPDF()


class Studloginfo(db.Model):
    studId = db.Column(db.Integer(), primary_key=True)
    stud_name = db.Column(db.String(45), nullable=False)
    stud_email = db.Column(db.String(60), unique=True, nullable=False)

    def Js_stud(self):
        return {"stud_name": self.stud_name, "stud_email": self.stud_email}


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


class Teacherlogin(db.Model):
    Te_id = db.Column(db.Integer(), primary_key=True)
    teacher_name = db.Column(db.String(60), nullable=False)
    teacher_email = db.Column(db.String(80), unique=True, nullable=False)
    t_password = db.Column(db.String(60), unique=True, nullable=False)

    def js_log(self):
        return {
            "id": self.Te_id, "teacher_name": self.teacher_name,
            "teacher_email": self.teacher_email,
            "t_password": self.t_password
        }


class Admininfo(db.Model):
    admin_name = db.Column(db.String(60), primary_key=True)
    admin_email = db.Column(db.String(80), unique=True, nullable=False)
    admin_pass = db.Column(db.String(60), unique=True, nullable=False)

    def js_add(self):
        return {
            "AdminD": self.admin_name,
            "Email": self.admin_email,
            "Password": self.admin_pass
        }


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


def gen_otp():
    otP = "".join([str(randint(1000, 9999)) for _ in range(1)])
    return otP


@app.route("/studlogin", methods=["GET", "POST"])
def studlogin():
    if request.method == "POST":
        studName = request.form.get("name")
        stdName1 = studName.split(" ")
        stdName2 = " ".join([i.capitalize() for i in stdName1])
        studEm = request.form.get("email")
        try:
            stud = Studloginfo.Js_stud(Studloginfo.query.filter_by(stud_name=stdName2).first())
        except AttributeError:
            flash("Invalid UserName or Email-ID")
            return redirect(url_for('studloginpg'))
        if stud["stud_name"] == stdName2 and stud["stud_email"] == studEm:
            otp1 = gen_otp()
            msg = Message("OTP", recipients=[stud["stud_email"]])
            msg.body = otp1
            mail.send(msg)
            en_otp = rsa.encrypt(otp1.encode(), publickey)
            session['response'] = {"Name": stdName2, "email": studEm, "OTP": en_otp}
            return render_template("studD/Otppchek.html")
        else:
            return render_template("studD/invalstud.html")


@app.route("/Otpstud", methods=["GET", "POST"])
def otppg():
    global otp_email, otp1, otp_name
    if request.method == "POST":
        studOTp = request.form.get("otp")
        otp1 = session['response']["OTP"]
        otp_name = session['response']["Name"]
        otp_email = session['response']["email"]
        de_otp = rsa.decrypt(otp1, privatekey).decode()
        if de_otp == studOTp:
            res_email = Studinfo.js_re(Studinfo.query.filter_by(Name=otp_name).first())
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


@app.route("/stafflogin", methods=["GET", "POST"])
def stafflogin():
    if "user_id" in session:
        session.pop("user_id", None)
    if request.method == 'POST':
        staff_user_name = request.form.get("stafname")
        staff_user_pass = request.form.get("pwds")
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


@app.route("/resultpg")
def resultpg():
    if "user_id" in session:
        name_data_set = [Studinfo.js_name(a)["Name"] for a in Studinfo.query.all()]
        paperp1_data_set = [Studinfo.js_p1(a)["Paper-1"][0:2] for a in Studinfo.query.all()]
        print(name_data_set, paperp1_data_set)
        p1_dict = {}
        for a, b in zip(name_data_set, paperp1_data_set):
            p1_dict[a] = int(b)
        plt.bar(p1_dict.keys(), [v / 80 for v in p1_dict.values()])
        plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
        plt.grid(axis='y')
        plt.savefig("paper1.jpg")

        # canvas = figureCanvas()
        # img = io.BytesIO(plt.grid(axis='y'))
        # fig.savefig(img)
        # img.seek(0)
        # return send_file(img, mimetype='img/png')
        return render_template("StaffD/reind.html", msg=plt.show())
    else:
        flash("Please login")
        return redirect("stafflogpg")


@app.route('/logout')
def stafflogout():
    if "user_id" in session:
        session.pop("user_id", None)
    return render_template("staffD/newstafflo.html")


@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    if "user_id2" in session:
        session.pop("user_id2", None)
    if request.method == 'POST':
        add_user_name = request.form.get("addname")
        add_user_pass = request.form.get("addpwds")
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


@app.route("/admindashpg")
def admindashpg():
    if "user_id2" in session:
        return render_template("staffD/adminpro.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/addstudinfoo", methods=['GET', 'POST'])
def addstudinfoo():
    if "user_id2" in session:
        if request.method == 'POST':
            stud_id_list = [Studinfo.js_st_id(a) for a in Studinfo.query.all()]
            new_stud_id = len(stud_id_list) + 1
            new_stud_name = request.form.get('studname')
            new_stud_name1 = new_stud_name.split(" ")
            new_stud_name2 = " ".join([i.capitalize() for i in new_stud_name1])
            new_stud_gen = request.form.get('gen')
            new_stud_sem = request.form.get('sem')
            new_stud_roll = request.form.get('rollno')
            new_stud_div = request.form.get('div')
            new_stud_p1 = request.form.get('p1')
            new_stud_p2 = request.form.get('p2')
            new_stud_p3 = request.form.get('p3')
            new_stud_p4 = request.form.get('p4')
            new_stud_p5 = request.form.get('p5')
            new_stud_percen = request.form.get('ptg')
            new_stud_result = request.form.get('stre')
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
            msgadd = "Student data added"
            return render_template("staffD/Adminstudinfoadd.html", msgadd=msgadd)
        return render_template("staffD/Adminstudinfoadd.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/updateinfo", methods=["GET", "POST"])
def updateinfo():
    if "user_id2" in session:
        if request.method == "POST":
            old_name = request.form.get("olname")
            new_name = request.form.get("nename")
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
            update_name = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_name.Name = new_name
            db.session.commit()
            fl_msg = "Student name updated!!"
            return render_template("staffD/studinfoupdate.html", fl_msg=fl_msg)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/updateinfop1", methods=["GET", "POST"])
def updateinfop1():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p1name")
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
            paper_01 = request.form.get("p1")
            paper_01_check = re.findall(r'[a-z A-Z]+', paper_01)
            valid = []
            if paper_01_check != valid:
                msg03 = 'please enter a valid input'
                return render_template("staffD/studinfoupdate.html", msg03=msg03)
            update_p1 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p1.Paper_1 = paper_01
            db.session.commit()
            msg04 = "Paper-1 marks updated for previous student"
            return render_template("staffD/studinfoupdate.html", msg04=msg04)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/updateinfop2", methods=["GET", "POST"])
def updateinfop2():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p2name")
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg21 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg21=msg21)
            paper_02 = request.form.get("p2")
            paper_02_check = re.findall(r'[a-z A-Z]+', paper_02)
            papar_list = []
            if paper_02_check != papar_list:
                msg22 = "please enter a valid input"
                return render_template("staffD/studinfoupdate.html", msg22=msg22)
            if len(paper_02) > 5:
                msg24 = "Please enter enter a valid input"
                return render_template("staffD/studinfoupdate.html", msg24=msg24)

            update_p2 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p2.Paper_2 = paper_02
            db.session.commit()
            msg23 = "Student Paper-2 marks updated!"
            return render_template("staffD/studinfoupdate.html", msg23=msg23)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/updateinfop3", methods=["GET", "POST"])
def updateinfop3():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p3name")
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg31 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg31=msg31)
            paper_03 = request.form.get("p3")
            paper_03_check = re.findall(r'[a-z A-Z]+', paper_03)
            paper_03_valid = []
            if paper_03_check != paper_03_valid:
                msg32 = "Please enter numerical input"
                return render_template("staffD/studinfoupdate.html", msg32=msg32)
            if len(paper_03) > 5:
                msg34 = "Please enter enter a valid input"
                return render_template("staffD/studinfoupdate.html", msg34=msg34)

            update_p3 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p3.Paper_3 = paper_03
            db.session.commit()
            msg33 = "Previous student marks updated!!"
            return render_template("staffD/studinfoupdate.html", msg33=msg33)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/updateinfop4", methods=["GET", "POST"])
def updateinfop4():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p4name")
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg41 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg41=msg41)
            paper_04 = request.form.get("p4")
            paper_04_check = re.findall(r'[a-z A-Z]+', paper_04)
            paper_04_valid = []
            if paper_04_check != paper_04_valid:
                msg42 = "Please enter numerical input"
                return render_template("staffD/studinfoupdate.html", msg42=msg42)
            if len(paper_04) > 5:
                msg44 = "Please enter enter a valid input"
                return render_template("staffD/studinfoupdate.html", msg44=msg44)

            update_p3 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p3.Paper_4 = paper_04
            db.session.commit()
            msg43 = "Previous student marks updated!!"
            return render_template("staffD/studinfoupdate.html", msg43=msg43)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/updateinfop5", methods=["GET", "POST"])
def updateinfop5():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p5name")
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                msg51 = "Student not found"
                return render_template("staffD/studinfoupdate.html", msg51=msg51)
            paper_05 = request.form.get("p5")
            paper_05_check = re.findall(r'[a-z A-Z]+', paper_05)
            paper_05_valid = []
            if paper_05_check != paper_05_valid:
                msg52 = "Please enter numerical input"
                return render_template("staffD/studinfoupdate.html", msg52=msg52)
            if len(paper_05) > 5:
                msg53 = "Please enter enter a valid input"
                return render_template("staffD/studinfoupdate.html", msg53=msg53)
            update_p5 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p5.Paper_5 = paper_05
            db.session.commit()
            msg54 = "Previous student marks updated!!"
            return render_template("staffD/studinfoupdate.html", msg54=msg54)
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route('/studdelpg', methods=["GET", "POST"])
def studdelpg():
    if "user_id2" in session:
        if request.method == "POST":
            del_info = request.form.get("studnamed")
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=del_info).first())
            except AttributeError:
                flash("Student data not found")
                return redirect("studdelpg")
            del_stu_in = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            db.session.delete(del_stu_in)
            db.session.commit()
            msg_de = "Student data deleted"
            return render_template("staffD/admindelinfo.html", msg_de=msg_de)
        return render_template("staffD/admindelinfo.html")
    else:
        flash("Admin login required")
    return render_template("staffD/Adminlog.html")


@app.route('/viewstud', methods=["GET", "POST"])
def viewstud():
    if "user_id2" in session:
        if request.method == "POST":
            stud_name_v = request.form.get("view")
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
            gen = show_stud["Gender"]
            sem = show_stud["Sem_1"]
            div = show_stud['Div']
            Paper_1 = show_stud["Paper_1"]
            Paper_2 = show_stud["Paper_2"]
            Paper_3 = show_stud["Paper_3"]
            Paper_4 = show_stud["Paper_4"]
            Paper_5 = show_stud["Paper_5"]
            per = show_stud["Overall_Percentage"]
            ress = show_stud["Stud_Result"]
            return render_template("staffD/studviewtable.html",
                                   Name=Name, gen=gen, sem=sem,
                                   div=div, Paper_1=Paper_1,
                                   Paper_2=Paper_2, Paper_3=Paper_3,
                                   Paper_4=Paper_4, Paper_5=Paper_5,
                                   per=per, ress=ress)
        return render_template("staffD/viewstud.html")

    return render_template("staffD/Adminlog.html")


@app.route('/adminlogout')
def adminlogout():
    if "user_id2" in session:
        session.pop("user_id2", None)
    return render_template("staffD/Adminlog.html")


if __name__ == "__main__":
    app.run(debug=True)
