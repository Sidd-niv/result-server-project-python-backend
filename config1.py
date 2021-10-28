import secrets
from random import randint
from Appp import app, db

# Configurations for application
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sidd@localhost/fyndacademy'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = secrets.token_hex(75)
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'fyndproject5@gmail.com'
app.config['MAIL_PASSWORD'] = 'Sidd@7021'
app.config['MAIL_DEFAULT_SENDER'] = 'fyndproject05@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False


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

# Function to generate random otp
def gen_otp():
    g_otp = "".join([str(randint(1000, 9999)) for _ in range(1)])
    return g_otp