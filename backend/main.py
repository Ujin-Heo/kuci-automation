from flask import request, jsonify
from config import app, db
from models import Contact

# 읽기(Read)
@app.route('/contacts', methods=['GET']) # /contacts <- end point
def get_contacts():
    pass

# 만들기(Create)
@app.route('/create_contact', methods=['POST'])
def create_contact():
    pass

# 수정하기(Update)
@app.route('/update_contact/<int:user_id>', methods=['PATCH'])
def update_contact(user_id):
    pass

# 삭제하기(Delete)
@app.route('/delete_contact/<int:user_id>', methods=['DELETE'])
def delete_contact(user_id):
    pass

# main.py를 직접 실행했을 때만 아래의 코드를 실행함. import 했을 때는 실행 안 함.
if __name__ == "__main__":
    # database가 이미 생성됐는지 확인 후 없다면 생성.
    with app.app_context():
        db.create_all()

    app.run(debug=True)
