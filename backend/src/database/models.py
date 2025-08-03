from sqlalchemy import String, JSON, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    sessionmaker,
    mapped_column,
    relationship,
)
from datetime import date, datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database.db")


class Base(DeclarativeBase):
    pass


class MetaData(Base):
    __tablename__ = "metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated_time: Mapped[datetime] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "lastUpdatedTime": self.last_updated_time.isoformat(),
            "startDate": self.start_date.isoformat(),
            "endDate": self.end_date.isoformat(),
        }


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    link: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # set one-to-many relationship (Board - Article)
    articles: Mapped[list["Article"]] = relationship(
        back_populates="board", cascade="all, delete-orphan"
    )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "articles": [article.to_json() for article in self.articles],
        }

    def write(self, file):
        for article in self.articles:
            file.write(f"📌 {article.title}\n")
            file.write(f"🔗 링크\n{article.link}\n\n")


class Article(Base):
    __tablename__ = "articles"
    __table_args__ = (
        UniqueConstraint("board_id", "title", name="uq_board_title"),
    )  # 같은 Board 안에서는 Article들의 title이 unique해야 함

    id: Mapped[int] = mapped_column(primary_key=True)
    pinned: Mapped[bool] = mapped_column(default=False, nullable=False)
    date: Mapped[str | None] = mapped_column(String(10), unique=False, nullable=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    link: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)

    # set one-to-many relationship (Board - Article)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), nullable=False)
    board: Mapped["Board"] = relationship(back_populates="articles")

    def to_json(self):
        return {
            "id": self.id,
            "pinned": self.pinned,
            "date": self.date,
            "title": self.title,
            "content": self.content,
            "link": self.link,
            "board_id": self.board_id,
        }


engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
