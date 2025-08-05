import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///' + os.path.join(BASEDIR, 'database.db')
