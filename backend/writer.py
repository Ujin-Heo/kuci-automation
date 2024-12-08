from models import Board

def write_announcement(month, week, writer):

    file_path = f'{month}월_{week}주차_전공소식공유.txt'

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"[2024 {month}월 {week}주차 전공소식 공유]\n") 
        file.write("\n안녕하세요.\n정보대학 제9대 학생회 '이음' 입니다.\n")
        file.write("금주의 전공소식을 공유드리니 많은 관심 부탁드립니다. 공지글의 링크로 들어가시면 더 자세한 정보를 확인하실 수 있습니다.\n")
        
        file.write("\n📢 일반공지\n")
        Board.query.filter_by(name='공지사항').first().write(file)
        # Board.query.filter_by(name='장학공지').first().write(file)

        file.write("\n📍 행사 및 공모전\n")
        Board.query.filter_by(name='행사 및 소식').first().write(file)
        Board.query.filter_by(name='진로정보(공모전)').first().write(file)

        file.write("\n💼 채용 및 인턴 모집\n")
        Board.query.filter_by(name='진로정보(채용)').first().write(file)
        Board.query.filter_by(name='진로정보(인턴)').first().write(file)

        file.write("\n📘 전공 관련 교육행사\n")
        Board.query.filter_by(name='진로정보(교육)').first().write(file)

        file.write(f"\n게시물 담당자: {writer}")
        file.write(f"\n게시물 책임자: 허우진")

    return file_path