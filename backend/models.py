from config import db

# One-to-Many Relationship
# Board - Article
 
class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    link = db.Column(db.String(100), unique=True, nullable=False)    
    
    # one-to-many relationship 설정하기
    articles = db.relationship('Article', backref='board', lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'articles': [article.to_json() for article in self.articles],
        }
    
class Article:
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), unique=False, nullable=True) # 날짜가 없는 상단 고정 게시물을 어떻게 처리할지 아직 미정.
    title = db.Column(db.String(100), unique=False, nullable=False)
    # content = db.Column(db.) 나중에 지피티 기능 만들 때 추가할 거임
    link = db.Column(db.String(100), unique=False, nullable=False)

    # Board에 연결해주는 Foreign key
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'date': self.date,
            'title': self.title,
            'link': self.link,
            'board_id': self.board_id,
        }