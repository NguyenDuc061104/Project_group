import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:ducan06112004@localhost:5432/teddydb'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False