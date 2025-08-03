from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from datetime import date
import asyncio

from ..database.models import get_db
from ..database.db import (
    get_metadata,
    delete_metadata,
    renew_metadata,
    get_boards_by_names,
    get_all_boards,
    initialize_boards,
    delete_articles,
)
from ..modules.scraper import scrape_board
from ..modules.board_infos import board_infos
from ..modules.ai_summarizer import summarize_and_save_to_db


router = APIRouter()


@router.get("/initialize_boards")
async def initialize(db: Session = Depends(get_db)):
    try:
        # DB 초기화하고 새로 만들기 (MetaData 초기화, Article/Board 모두 삭제 후 Board 새로 만들기)
        delete_metadata(db)
        initialize_boards(db)

        return {"message": "[서버 메시지] DB를 성공적으로 초기화했습니다."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


# DB에 저장된 게시판/게시물 데이터 불러오기
@router.get("/get_boards")
async def get_boards(db: Session = Depends(get_db)):
    try:
        metadata_row = get_metadata(db)
        json_meta_data = metadata_row.to_json() if metadata_row else None

        boards = get_all_boards(db)
        json_boards = [board.to_json() for board in boards]

        return {
            "message": "[서버 메시지] 게시물을 성공적으로 불러왔습니다.",
            "metaData": json_meta_data,
            "boards": json_boards,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.websocket("/update_boards")
async def update_boards(
    start_date: date,
    end_date: date,
    websocket: WebSocket,
    db: Session = Depends(get_db),
):
    try:
        # MetaData 저장
        renew_metadata(db, start_date, end_date)

        # 2024-01-01 형태의 날짜를 2024.01.01 형태로 변환(정보대 홈피 사이트와 동일하게)
        date_range = (
            start_date.strftime("%Y.%m.%d"),
            end_date.strftime("%Y.%m.%d"),
        )

        # 저장된 게시물 모두 삭제(게시판은 그대로 둠)
        delete_articles(db)

        await websocket.accept()
        tasks = [
            scrape_board(board_info, date_range, db, websocket)
            for board_info in board_infos
        ]
        await asyncio.gather(*tasks, return_exceptions=True)
        await websocket.send_json(
            {
                "status": "done",
                "message": "[서버 메시지] 모든 게시판 스크래핑을 완료하였습니다.",
            }
        )
        await websocket.close()

    # scrape_board 호출 이전 과정에서 에러가 발생하면 아래에서 예외처리됨
    except ValueError as ve:
        await websocket.send_json(
            {"status": "error", "message": f"[서버 메시지] 입력 값 오류: {str(ve)}"}
        )
        await websocket.close()

    except Exception as e:
        await websocket.send_json(
            {"status": "error", "message": f"[서버 메시지] 서버 오류: {str(e)}"}
        )
        await websocket.close()


@router.websocket("/summarize")
async def summarize(websocket: WebSocket, db: Session = Depends(get_db)):
    try:
        await websocket.accept()
        boards_to_summarize = get_boards_by_names(
            db,
            [
                "공지사항",
                "행사 및 소식",
                "진로정보(공모전)",
                "진로정보(교육)",
            ],
        )

        tasks = [
            summarize_and_save_to_db(article, db, websocket)
            for board in boards_to_summarize
            for article in board.articles
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

        await websocket.send_json(
            {
                "status": "done",
                "message": "[서버 메시지] 모든 게시물 요약을 완료하였습니다.",
            }
        )
        await websocket.close()

    # summarize_and_save_to_db 호출 이전 과정에서 에러가 발생하면 아래에서 예외처리됨
    except ValueError as ve:
        await websocket.send_json(
            {"status": "error", "message": f"[서버 메시지] 입력 값 오류: {str(ve)}"}
        )
        await websocket.close()

    except Exception as e:
        await websocket.send_json(
            {"status": "error", "message": f"[서버 메시지] 서버 오류: {str(e)}"}
        )
        await websocket.close()
