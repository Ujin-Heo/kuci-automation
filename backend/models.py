from config import db

class MetaData(db.Model):
    __tablename__ = 'metadata'

    id = db.Column(db.Integer, primary_key=True)
    last_updated_time = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'lastUpdatedTime': self.last_updated_time.isoformat(),
            'startDate': self.start_date.isoformat(),
            'endDate': self.end_date.isoformat()
        }


# One-to-Many Relationship
# Board - Article
 
class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    link = db.Column(db.String(100), unique=True, nullable=False)    
    
    # one-to-many relationship 설정하기
    articles = db.relationship('Article', backref='board', lazy=True)

    def __init__(self, name, link):
        self.name = name
        self.link = link

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'articles': [article.to_json() for article in self.articles],
        }
    
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    pinned = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.String(10), unique=False, nullable=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    # content = db.Column(db.) 나중에 지피티 기능 만들 때 추가할 거임
    link = db.Column(db.String(100), unique=False, nullable=False)

    # Board에 연결해주는 Foreign key
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)

    def __init__(self, pinned, date, title, link, board_id):
        self.pinned = pinned
        self.date = date
        self.title = title
        self.link = link
        self.board_id = board_id

    def to_json(self):
        return {
            'id': self.id,
            'date': self.date,
            'title': self.title,
            'link': self.link,
            'board_id': self.board_id,
        }