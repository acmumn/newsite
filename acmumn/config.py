import os

class Config():
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

