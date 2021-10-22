import secrets
from flask import Flask, render_template, request, session, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from random import randint
from flask_login import UserMixin, LoginManager, current_user
from flask_admin import Admin

# from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
db = SQLAlchemy(app)
login = LoginManager()
login.init_app(app)
# admin = Admin(app)
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


class Teacherlogin(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    teacher_name = db.Column(db.String(60), nullable=False)
    teacher_email = db.Column(db.String(80), unique=True, nullable=False)
    t_password = db.Column(db.String(60), unique=True, nullable=False)


# admin.add_view(ModelView(Teacherlogin, db.session))


@app.route("/")
def home():
    print(app.config)
    return render_template("oppstudshaff.html")


@app.route("/studotplog")
def studlogpa():
    return render_template("studD/studentlg.html")


@app.route("/staffloog")
def stafflogpa():
    return render_template("staffD/Stafflogin.html")


@app.route("/inv_otp")
def otp_re():
    return render_template("studD/Otppchek.html")


@login.user_loader
def load_user(user_id):
    return Teacherlogin.query.get(user_id)


def gen_otp():
    otP = "".join([str(randint(1000, 9999)) for _ in range(1)])
    return otP


@app.route("/studinfo", methods=["GET", "POST"])
def stud_info():
    if request.method == "POST":
        studName = request.form.get("name")
        stdName1 = studName.split(" ")
        stdName2 = " ".join([i.capitalize() for i in stdName1])
        studEm = request.form.get("email")
        try:
            stud = Studloginfo.Js_stud(Studloginfo.query.filter_by(stud_name=stdName2).first())
        except AttributeError:
            return render_template("studD/invalstud.html")
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
            return render_template("studD/invalidstudotp.html")


if __name__ == "__main__":
    app.run(debug=True)
