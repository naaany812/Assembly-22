import os

current_path = os.path.dirname(os.path.realpath(__file__))
db_path = "sqlite:///" + current_path + "\\test.db"


class Config:
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Assembly-22 is the last project in this course"
