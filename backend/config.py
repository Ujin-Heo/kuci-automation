from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy # ORM: using python class for database
from flask_cors import CORS # cross origin requests

app = Flask(__name__)

# expose_headers=["Content-Disposition"]를 추가하면 파일 다운로드 시 백엔드에서 파일명을 설정할 수 있습니다.
CORS(
    app,
    origins=["http://127.0.0.1:5173", "https://kuci-automation-1.onrender.com"],
    methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"]
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)