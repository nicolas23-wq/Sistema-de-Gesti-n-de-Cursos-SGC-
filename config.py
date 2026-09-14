import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-por-defecto")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///gestion_cursos.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
