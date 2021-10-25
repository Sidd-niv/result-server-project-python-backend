import secrets
import os
import re
from flask import Flask, render_template, request, session, flash, redirect, url_for, Response
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from random import randint
from mail_pdff_den import *
import matplotlib.pyplot as plt

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sidd@localhost/fyndacademy'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = secrets.token_hex(75)
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
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
    if 'response' in session:
        session.pop('response', None)
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
            otp = gen_otp()
            msg = Message("OTP", recipients=[stud["stud_email"]])
            msg.body = otp
            mail.send(msg)
            session['response'] = {"Name": stdName2, "email": studEm, "OTP": otp}
            return render_template("studD/Otppchek.html")
        else:
            return render_template("studD/invalstud.html")


@app.route("/Otpstud", methods=["GET", "POST"])
def otppg():
    global otp_email, otp, otp_name
    if request.method == "POST":
        studOTp = request.form.get("otp")
        if 'response' in session:
            otp = session['response']["OTP"]
            otp_name = session['response']["Name"]
            otp_email = session['response']["email"]
        if otp == studOTp:
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
        data_name_set1 = [Studinfo.js_name(a) for a in Studinfo.query.all()]
        data_set_name = []
        for i in range(len(data_name_set1)):
            data_set_name.append(data_name_set1[i]["Name"])
        data_p1_set = [Studinfo.js_p1(a) for a in Studinfo.query.all()]
        data_set_p1_list = []
        datasetp_1 = []
        for i in range(len(data_p1_set)):
            data_set_p1_list.append(data_p1_set[i]["Paper-1"])
        for j in range(len(data_set_p1_list)):
            datasetp_1.append(int(data_set_p1_list[j][0:2]))
        left_edges = datasetp_1
        height = data_set_name
        plt.bar(left_edges, height)
        plt.title("Percentage Graph")
        plt.xlabel("Students")
        plt.ylabel("Percentage")
        plt.savefig("Paper-1.png")

        return render_template("StaffD/reind.html")
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
            return redirect(url_for('adminres'))
        else:
            flash("Invalid Username or Password")
            return redirect(url_for('Adminlogpg'))
    else:
        return render_template("staffD/Adminlog.html")


@app.route("/adminres")
def adminres():
    if "user_id2" in session:
        # data_Set1 = Studinfo.js_st_name_paper1(Studinfo)
        # plt.plot()
        # plt.title("Student graph")
        # plt.xlabel("Student")
        # plt.ylabel("Marks")
        # plt.xlim(xmin=0, xmax=7)
        # plt.ylim(ymin=1, ymax=100)
        # plt.grid(True)
        # plt.show()
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
            old_stud_name = [Studinfo.js_st_name(a) for a in Studinfo.query.all()]
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
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=old_name).first())
            except AttributeError:
                flash("Invalid Student Name")
                return redirect(url_for('updateinfo'))
            update_name = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_name.Name = new_name
            db.session.commit()
            flash("Student name updated!!")
            return redirect(url_for('updateinfo'))
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
            if not name_check:
                flash('please enter a valid name input')
                return redirect("updateinfop1")
            paper_01 = request.form.get("p1")
            paper_01_check = re.findall(r'[a-z A-Z]+', paper_01)
            if not paper_01_check:
                flash('please enter a valid input')
                return redirect("updateinfop1")
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                flash("Invalid Student Name")
                return redirect("updateinfop1")
            update_p1 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p1.Paper_1 = paper_01
            db.session.commit()
            flash("Pervious marks updated")
            return redirect("updateinfop1")
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/updateinfop2", methods=["GET", "POST"])
def updateinfop2():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p2name")
            name_check = re.findall(r'[0-9]+', name)
            if not name_check:
                flash('please enter a valid name input')
                return render_template("staffD/studinfoupdate.html")
            paper_02 = request.form.get("p2")
            paper_01_check = re.findall(r'[a-z A-Z]+', paper_02)
            if not paper_01_check:
                flash('please enter a valid input')
                return render_template("staffD/studinfoupdate.html")
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                flash("Invalid Student Name")
                return redirect(url_for('updateinfop2'))
            update_p2 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p2.Paper_2 = paper_02
            db.session.commit()
            flash("Previous student name updated!!")
            return redirect(url_for('updateinfop2'))
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route("/updateinfop3", methods=["GET", "POST"])
def updateinfop3():
    if "user_id2" in session:
        if request.method == "POST":
            name = request.form.get("p3name")
            name_check = re.findall(r'[0-9]+', name)
            if not name_check:
                flash('please enter a valid name input')
                return render_template("staffD/studinfoupdate.html")
            paper_03 = request.form.get("p3")
            paper_01_check = re.findall(r'[a-z A-Z]+', paper_03)
            if not paper_01_check:
                flash('please enter a valid input')
                return render_template("staffD/studinfoupdate.html")
            try:
                check_data = Studinfo.js_re(Studinfo.query.filter_by(Name=name).first())
            except AttributeError:
                flash("Invalid Student Name")
                return render_template("staffD/studinfoupdate.html")
            update_p3 = Studinfo.query.filter_by(stud_id=check_data["stud_id"]).first()
            update_p3.Paper_3 = paper_03
            db.session.commit()
            flash("Previous student name updated!!")
            return render_template("staffD/studinfoupdate.html")
        return render_template("staffD/studinfoupdate.html")
    else:
        flash("Admin login required")
        return render_template("staffD/Adminlog.html")


@app.route('/adminlogout')
def adminlogout():
    if "user_id2" in session:
        session.pop("user_id2", None)
    return render_template("staffD/Adminlog.html")


if __name__ == "__main__":
    app.run(debug=True)

# if request.form.get("p_1") == "p_1":
#     name = request.form.get('p1name')
#     paper_01 = request.form.get('p1')
#     try:
#         update_reso = Studinfo.query.filter_by(Name=name).first()
#     except AttributeError:
#         flash("Invalid Student Name")
#         return redirect(url_for('updateinfo'))
#     update_reso.Paper_1 = paper_01
#     db.session.commit()
#     return redirect(url_for('updateinfo'))
# if request.form.get("p_2") == "p_2":
#     name = request.form.get('p2name')
#     paper_02 = request.form.get('p2')
#     try:
#         update_reso = Studinfo.query.filter_by(Name=name).first()
#     except AttributeError:
#         flash("Invalid Student Name")
#         return redirect(url_for('updateinfo'))
#     update_reso.Paper_2 = paper_02
#     db.session.commit()
#     return redirect(url_for('updateinfo'))
# if request.form.get("p_3") == "p_3":
#     name = request.form.get('p3name')
#     paper_03 = request.form.get('p3')
#     try:
#         update_reso = Studinfo.query.filter_by(Name=name).first()
#     except AttributeError:
#         flash("Invalid Student Name")
#         return redirect(url_for('updateinfo'))
#     update_reso.Paper_3 = paper_03
#     db.session.commit()
#     return redirect(url_for('updateinfo'))
# if request.form.get("p_4") == "p_4":
#     name = request.form.get('p4name')
#     paper_04 = request.form.get('p4')
#     try:
#         update_reso = Studinfo.query.filter_by(Name=name).first()
#     except AttributeError:
#         flash("Invalid Student Name")
#         return redirect(url_for('updateinfo'))
#     update_reso.Paper_4 = paper_04
#     db.session.commit()
#     return redirect(url_for('updateinfo'))
# if request.form.get("p_5") == "p_5":
#     name = request.form.get('p5name')
#     paper_05 = request.form.get('p5')
#     try:
#         update_reso = Studinfo.query.filter_by(Name=name).first()
#     except AttributeError:
#         flash("Invalid Student Name")
#         return redirect(url_for('updateinfo'))
#     update_reso.Paper_5 = paper_05
#     db.session.commit()
#     return redirect(url_for('updateinfo'))
# return render_template("staffD/studinfoupdate.html")
