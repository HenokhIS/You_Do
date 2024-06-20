import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///youdo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    JWT_SECRET_KEY = 'd63e2651d0ecf2446ddb86938951e548c22fca52fc14b8d6'
