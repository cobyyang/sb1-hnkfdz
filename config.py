import os
from dotenv import load_load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///leads.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False