import secrets


class Config:
    DEBUG = False
    TESTING = False
    # UPLOADS
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:Sidd@localhost/fyndacademy'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = secrets.token_hex(75)
    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = 'fyndproject05@gmail.com'
    # MAIL_PASSWORD = 'Fyndpro@05'
    # MAIL_DEFAULT_SENDER = 'fyndproject05@gmail.com'
    # MAIL_MAX_EMAILS = None
    # MAIL_SUPPRESS_SEND = False
    # MAIL_ASCII_ATTACHMENTS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Sidd@localhost/fyndacademy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(75)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'fyndproject05@gmail.com'
    MAIL_PASSWORD = 'Fyndpro@05'
    MAIL_DEFAULT_SENDER = 'fyndproject05@gmail.com'
    MAIL_MAX_EMAILS = None
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING = True
