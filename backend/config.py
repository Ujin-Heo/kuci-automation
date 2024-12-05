from flask import Flask
from flask_sqlalchemy import SQLAlchemy # ORM: using python class for database
from flask_cors import CORS # cross origin requests

app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
