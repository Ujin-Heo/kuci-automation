from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import date
import asyncio

from ..database.models import get_db, Board, MetaData
from ..database.db import (
    get_metadata,
    delete_metadata,
    renew_metadata,
    get_all_boards,
    initialize_boards,
    delete_articles,
)
from ..modules.scraper import scrape_board
from ..modules.board_infos import board_infos


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


# DB에 저장된 게시판/게시글 데이터 불러오기
@router.get("/get_boards")
async def get_boards(db: Session = Depends(get_db)):
    try:
        metadata_row = get_metadata(db)
        json_meta_data = metadata_row.to_json() if metadata_row else None

        boards = get_all_boards(db)
        json_boards = [board.to_json() for board in boards]

        return {
            "message": "[서버 메시지] 게시글을 성공적으로 불러왔습니다.",
            "metaData": json_meta_data,
            "boards": json_boards,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


# 입력된 날짜 범위의 게시글 스크랩해서 DB에 저장하기
# @router.get("/update_boards")
# async def update_boards(
#     start_date: date, end_date: date, db: Session = Depends(get_db)
# ):
#     try:
#         # MetaData 저장
#         renew_metadata(db, start_date, end_date)

#         # 2024-01-01 형태의 날짜를 2024.01.01 형태로 변환(정보대 홈피 사이트와 동일하게)
#         date_range = (
#             start_date.strftime("%Y.%m.%d"),
#             end_date.strftime("%Y.%m.%d"),
#         )

#         # 저장된 게시글 모두 삭제(게시판은 그대로 둠)
#         delete_articles(db)

#         # 날짜 범위 내의 게시글 새로 스크래핑
#         scrape_boards(db, board_infos, date_range)

#         return JSONResponse(
#             content={"message": "[서버 메시지] 게시판 스크래핑에 성공하였습니다."},
#             status_code=status.HTTP_201_CREATED,
#         )

#     except ValueError as ve:
#         raise HTTPException(
#             status_code=400, detail=f"[서버 메시지] 입력 값 오류: {str(ve)}"
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"[서버 메시지] 서버 오류: {str(e)}"
#         )


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

        # 저장된 게시글 모두 삭제(게시판은 그대로 둠)
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
                "message": "[서버 메시지] 모든 게시판 스크래핑에 성공하였습니다.",
            }
        )
        await websocket.close()

    # TODO 에러 핸들링 수정하기 (UpdateBoardsForm.jsx도 참고)
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
