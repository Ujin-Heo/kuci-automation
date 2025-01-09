from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy # ORM: using python class for database
from flask_cors import CORS # cross origin requests

app = Flask(__name__)

CORS(app, origins=["https://kuci-automation-1.onrender.com"], expose_headers=["Content-Disposition"]) # expose_headers=["Content-Disposition"]를 넣어야 파일 다운로드 시 파일명 벡엔드에서 설정가능함.

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.after_request
def apply_cors_headers(response):
    origin = request.headers.get('Origin')
    allowed_origins = ["http://127.0.0.1:5173", "https://kuci-automation-1.onrender.com"]
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS,PUT,DELETE"
    return response
