import secrets
from Appp import app

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


