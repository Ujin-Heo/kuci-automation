from flask import request, jsonify, send_file, after_this_request
from config import app, db
from board_infos import board_infos
from scraper import scrape_boards
from writer import write_announcement
from models import MetaData, Board, Article

# 내가 새로 만든 라이브러리
from scraper import scrape_boards # 게시판 스크래핑에 사용
from writer import write_announcement # 공지글 txt 파일 작성에 사용

# 기타 유틸리티 라이브러리 (파이썬 기본 제공)
from datetime import datetime, timedelta
import os

# 읽기(Read)
@app.route('/boards', methods=['GET']) # /boards <- end point
def get_boards():
    metadata_row = MetaData.query.first()
    json_meta_data = metadata_row.to_json() if metadata_row else None

    boards = Board.query.all()
    json_boards = [board.to_json() for board in boards]

    return jsonify({'metaData': json_meta_data,
                    'boards': json_boards},), 200

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

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

    # MetaData 저장
    db.session.query(MetaData).delete()  # Delete all rows from MetaData (MetaData 초기화)
    metadata = MetaData(
        last_updated_time=datetime.now() + timedelta(hours=31),
        start_date=start_date_obj,
        end_date=end_date_obj
    )
    db.session.add(metadata)
    db.session.commit()

    # 2024-01-01 형태의 날짜를 2024.01.01 형태로 변환(정보대 홈피 사이트와 동일하게)
    date_range = (
        start_date_obj.strftime('%Y.%m.%d'),
        end_date_obj.strftime('%Y.%m.%d')
    )

    # 데이터베이스 초기화하기(저장된 게시글, 게시판 모두 삭제)
    db.session.query(Article).delete()
    # db.session.query(Board).delete()

    try:
        scrape_boards(board_infos, date_range)
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    return jsonify({'message': '게시판이 성공적으로 업데이트되었습니다.'}), 201

# 공지글 작성하기
@app.route('/announcement', methods=['POST'])
def announcement():
    month = request.json.get('month')
    week = request.json.get('week')
    writer = request.json.get('writer')

    if not month or not week or not writer:
        return (
            jsonify({'message': 'You must include a start date, an end date, and a writer.'}),
            400,
        )

    file_path = write_announcement(month, week, writer)

    # 프론트엔드로 파일 보낸 후 벡엔드 서버에서는 삭제
    @after_this_request
    def remove_file(response):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            app.logger.error(f"Error removing file {file_path}: {e}")
        return response
    
    # Send the file
    return send_file(
        file_path,
        as_attachment=True,  # Ensure the file is downloaded by the client
        # download_name=f'{month}월_{week}주차_전공소식공유.txt',  # Custom filename
        mimetype="text/plain"
    )

# app.py를 직접 실행했을 때만 아래의 코드를 실행함. import 했을 때는 실행 안 함.
if __name__ == "__main__":
    # database가 이미 생성됐는지 확인 후 없다면 생성.
    with app.app_context():
        db.create_all()

    app.run(debug=True)
