import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'This-will-be-automated-later'

    # TODO maybe hardcode the postgre db info?
    POSTGRES_URL = os.environ.get("POSTGRES_URL")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PW = os.environ.get("POSTGRES_PW")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")

    DB_URL = 'postgresql://{user}:{password}@{url}/{db}'.format(user=POSTGRES_USER,password=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False