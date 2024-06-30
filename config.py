import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///youdo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    JWT_SECRET_KEY = 'd1a7e6f8b3c4027e9dbf4b7fe3c2d0eaf7d9617ff279fbb3a6c9a49cf8c1e4d2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'timeout': 30  # timeout dalam detik
        }
    }
