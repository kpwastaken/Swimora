import os

class Config:
    SECRET_KEY = "swimora-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///swimora.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

