from flask import request, jsonify
from config import app, db
from scraper import scrape_boards
from models import Board
from datetime import datetime

board_infos = {
    '공지사항': ('공지사항', 'https://info.korea.ac.kr/info/board/notice_under.do'),
    '장학공지': ('장학공지', 'https://info.korea.ac.kr/info/board/scholarship_under.do'),
    '행사 및 소식': ('행사 및 소식', 'https://info.korea.ac.kr/info/board/news.do'),
    '진로정보(채용)': ("진로정보(채용)", 'https://info.korea.ac.kr/info/board/course_job.do'),
    '진로정보(교육)': ("진로정보(교육)", 'https://info.korea.ac.kr/info/board/course_program.do'),
    '진로정보(인턴)': ("진로정보(인턴)", 'https://info.korea.ac.kr/info/board/course_intern.do'),
    '진로정보(공모전)': ("진로정보(공모전)", 'https://info.korea.ac.kr/info/board/course_competition.do'),
}

# 읽기(Read)
@app.route('/boards', methods=['GET']) # /boards <- end point
def get_boards():
    boards = Board.query.all()
    json_boards = list(map(lambda x:x.to_json(), boards))
    return jsonify({'boards': json_boards}), 200

# 만들기(Create)
@app.route('/update_boards', methods=['POST'])
def update_boards():

    start_date = request.json.get('startDate') # get: 데이터가 없으면 None 반환
    end_date = request.json.get('endDate')

    if not start_date or not end_date:
        return (
            jsonify({'message': 'You must include a start date and an end date.'}),
            400,
        )

    # 2024-01-01 형태의 날짜를 2024.01.01 형태로 변환(정보대 홈피 사이트와 동일하게)
    start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y.%m.%d')
    end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y.%m.%d')
    date_range = (start_date_formatted, end_date_formatted)

    # 데이터베이스 초기화하기 (나중에 drop_all, create_all 대신 Flask-Migrate 코드로 바꿔보기)
    db.session.remove()
    db.drop_all()
    db.create_all()

    try:
        scrape_boards(board_infos, date_range)
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    return jsonify({'message': '게시판이 성공적으로 업데이트되었습니다.'}), 201

# 공지글 작성하기
@app.route('/write_announcement', methods=['POST'])
def write_announcement():
    pass

# PPT 생성하기
@app.route('/make_ppt', methods=['POST'])
def make_ppt():
    pass

# # 수정하기(Update)
# @app.route('/update_contact/<int:user_id>', methods=['PATCH'])
# def update_contact(user_id):
#     pass

# # 삭제하기(Delete)
# @app.route('/delete_contact/<int:user_id>', methods=['DELETE'])
# def delete_contact(user_id):
#     pass

# main.py를 직접 실행했을 때만 아래의 코드를 실행함. import 했을 때는 실행 안 함.
if __name__ == "__main__":
    # database가 이미 생성됐는지 확인 후 없다면 생성.
    with app.app_context():
        db.create_all()

    app.run(debug=True)
