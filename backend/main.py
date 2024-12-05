from flask import request, jsonify
from config import app, db
from scraper import scrape_boards

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
@app.route('/contacts', methods=['GET']) # /contacts <- end point
def get_contacts():
    pass

# 만들기(Create)
@app.route('/update_boards', methods=['POST'])
def update_boards():
    try:
        scrape_boards(board_infos)
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    return jsonify({'message': '게시판이 성공적으로 업데이트되었습니다.'}), 201

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
