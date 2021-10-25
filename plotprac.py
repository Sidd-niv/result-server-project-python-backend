from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sidd@localhost/fyndacademy'


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

    def js_name(self):
        return {"Name": self.Name}

    def js_p1(self):
        return {"Paper-1": self.Paper_1}


data_name_set1 = [Studinfo.js_name(a) for a in Studinfo.query.all()]
data_set_name = []
for i in range(len(data_name_set1)):
    data_set_name.append(data_name_set1[i]["Name"])


data_p1_set = [Studinfo.js_p1(a) for a in Studinfo.query.all()]
data_set_p1 = []
datasetp_1 = []

for i in range(len(data_p1_set)):
    data_set_p1.append(data_p1_set[i]["Paper-1"])
for j in range(len(data_set_p1)):
    datasetp_1.append(int(data_set_p1[j][0:2]))


def Bar_plot():
    left_edges = datasetp_1
    height = data_set_name
    plt.bar(left_edges, height)
    plt.title("Percentage Graph")
    plt.xlabel("Students")
    plt.ylabel("Percentage")
    plt.savefig("Paper-1.png")

Bar_plot()


