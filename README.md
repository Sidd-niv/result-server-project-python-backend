# Exam-results-for-students-and-analytic-reults-for-staff

Exam and analytic results is an web-application which provides features like :
1) Authentication for student through OTP to send there result 
2) Display result for each student on there verified email.
3) Analytic results for staff to evaluate there students performance throughout the academics  



# Project Result Server

## Package Installation

```bash
pip os 
pip install flask 
pip install flask-SQLalchemy
pip install flask-mail
pip install FPDF
pip install re  
pip install secrets
pip install random
pip install matplotlib.pyplot
pip install rsa
pip install matplotlib
```
## Phase-1
# Task 1
* Task-1 was to generate OTP and send it to register student email address
* By using flask-mail, an otp is send to student via email 

# Task 2 
*Task-2 was to send result via email
-By flask-mail, result was send successfully via email in pdf format after verification through email

## Phase-2
*Task-1 was to build login-logout for staff/Teachers 
-Which is done by sessions 
*Task-2 was to generate graph to analyse each marks in each paper in percentage format.
-Graphs were generated using student data retrieved from database and with the help of matplotlib graphs were displayed on frontend 

## Phase-3
*Task -1 was to build login and logout for admin
-Which is done by sessions 
*Task-2 was to give CURD to admin
-For both students and teacher login
and student database


