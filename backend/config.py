from flask import Flask
from flask_sqlalchemy import SQLAlchemy # ORM: using python class for database
from flask_cors import CORS # cross origin requests

app = Flask(__name__)

CORS(app, origins=["https://kuci-automation-1.onrender.com", "http://127.0.0.1:5173"], expose_headers=["Content-Disposition"]) # expose_headers=["Content-Disposition"]를 넣어야 파일 다운로드 시 파일명 벡엔드에서 설정가능함.

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
