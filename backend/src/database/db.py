from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from datetime import date, datetime

from .models import MetaData, Board, Article
from ..modules.board_infos import board_infos


# MetaData related operations #########################################
def get_metadata(db: Session):
    stmt = select(MetaData)
    return db.scalars(stmt).first()


def delete_metadata(db: Session):
    db.execute(delete(MetaData))


def renew_metadata(db: Session, start_date: date, end_date: date):
    # delete all existing MetaData

    # SQLAlchemy ORM style
    # stmt = select(MetaData)
    # for row in db.scalars(stmt):
    #     db.delete(row)

    # SQLAlchemy CORE stlye -> faster
    db.execute(delete(MetaData))
    db.flush()

    # insert new MetaData
    metadata = MetaData(
        last_updated_time=datetime.now(),
        start_date=start_date,
        end_date=end_date,
    )
    db.add(metadata)
    db.commit()


# Board related operations ############################################
def get_board_by_name(db: Session, name: str):
    stmt = select(Board).where(Board.name == name)
    return db.scalars(stmt).first()


def get_boards_by_names(db: Session, names: list[str]) -> list[Board]:
    stmt = select(Board).where(Board.name.in_(names))
    return db.scalars(stmt).all()


def get_all_boards(db: Session):
    stmt = select(Board)
    return db.scalars(stmt)


def delete_boards(db: Session):
    boards = db.scalars(select(Board)).all()
    for board in boards:
        db.delete(board)
        # cascade: "all, delete-orphans" 때문에 제거되는 Board 안의 Article도 자동으로 삭제됨
    db.commit()


def initialize_boards(db: Session):
    db.execute(delete(Board))
    db.execute(delete(Article))
    for name, link in board_infos:
        db.add(Board(name=name, link=link))
    db.commit()


# Article related operations ##########################################
def delete_articles(db: Session):
    db.execute(delete(Article))
