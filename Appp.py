import secrets
from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from random import randint

# from flask_admin.contrib.sqla import ModelView

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
    Sem_1 = db.Column(db.Integer(), unique=False, nullable=False)
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
                "Sem_1": self.Sem_1, "Roll_no": self.Roll_no,
                "Div": self.Div, "Paper_1": self.Paper_1,
                "Paper_2": self.Paper_2, "Paper_3": self.Paper_3,
                "Paper_4": self.Paper_4, "Paper_5": self.Paper_5,
                "Overall_Percentage": self.Overall_Percentage,
                "Stud_Result": self.Stud_Result}



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


@app.route("/")
def home():
    return render_template("oppstudshaff.html")


@app.route("/studloginpg")
def studloginpg():
    return render_template("studD/newstudentlog.html")


@app.route("/stafflogpg")
def stafflogpg():
    return render_template("staffD/newstafflo.html")


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
    global otp, otp_name, otp_email
    if request.method == "POST":
        studOTp = request.form.get("otp")
        if 'response' in session:
            otp = session['response']["OTP"]
            otp_name = session['response']["Name"]
            otp_email = session['response']["email"]
        if otp == studOTp:
            res_email = Studinfo.js_re(Studinfo.query.filter_by(Name=otp_name).first())
            final_mail_msg = f"Name: {res_email['Name']} |Roll No: {res_email['Roll_no']} |Div: {res_email['Div']} |Sem: {res_email['Sem_1']}\n" \
                             f"Paper-1 Marks: {res_email['Paper_1']}\n" \
                             f"Paper-2 Marks: {res_email['Paper_2']}\n" \
                             f"Paper-3 Marks: {res_email['Paper_3']}\n" \
                             f"Paper-4 Marks: {res_email['Paper_4']}\n" \
                             f"Paper-5 Marks: {res_email['Paper_5']}\n" \
                             f"Percentage: {res_email['Overall_Percentage']}\n" \
                             f"---------------------------------------\n" \
                             f"Result: {res_email['Stud_Result']}"
            msg = Message("FYND SEM-1 Result", recipients=[otp_email])
            msg.body = final_mail_msg
            mail.send(msg)
            if 'response' in session:
                session.pop('response', None)
            return render_template("studD/email_re.html")
        else:
            flash('Please enter a valid OTP')
            return redirect(url_for('invalidotppg'))


@app.route("/stafflogin", methods=["GET", "POST"])
def stafflogin():
    if request.method == 'POST':
        staff_user_name = request.form.get("stafname")
        staff_user_pass = request.form.get("pwds")
        if "user_id" in session:
            session.pop("user_id", None)
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
        return render_template("StaffD/reind.html")
    else:
        flash("Please login")
        return redirect("stafflogpg")

@app.route('/logout')
def stafflogout():
    if "user_id" in session:
        session.pop("user_id", None)
    return render_template("staffD/newstafflo.html")







if __name__ == "__main__":
    app.run(debug=True)
