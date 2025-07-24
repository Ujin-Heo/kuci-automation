from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy # ORM: using python class for database
from flask_cors import CORS # cross origin requests

from flask import Flask # Flask: 파이썬 웹 프레임워크
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy: 파이썬 class 문법을 사용해서 데이터베이스를 다룰 수 있게 해주는 라이브러리
# 그냥 SQLAlchemy도 있지만, flask_sqlalchemy는 Flask에서 더 사용하기 쉽게 만들어진 버전의 SQLAlchemy임. 
# ORM (Object Relational Mapping): 파이썬의 class와 같은 객체지향 문법을 사용해서 데이터베이스를 다루게 해주는 기술. SQLAlchemy도 ORM의 한 종류임.
# ORM을 사용하면 SQL 언어를 따로 안 배워도 파이썬 코드로 데이터베이스를 다룰 수 있음.
from flask_cors import CORS # CORS (Cross Origin Resource Sharing): 벡엔드는 Flask, 프론트엔드는 React로 만들었는데, 이 둘은 다른 origin이기 때문에 CORS 설정을 해줘야 함. 대충 아래처럼 갖다쓰면 알아서 잘 해줌.

CORS(app, origins=["https://kuci-automation-1.onrender.com"]) # expose_headers=["Content-Disposition"]를 넣어야 파일 다운로드 시 파일명 벡엔드에서 설정가능함.

CORS(app) # 이렇게 하면 CORS 설정이 완료됨. 이제 프론트엔드에서 벡엔드로 요청을 보내도 에러가 안 남.

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db" # 사용할 데이터베이스를 sqllite로 설정해줌. instance 폴더에 mydatabase.db 파일이 생성됨.
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
