from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
import asyncio

from ..database.models import get_db, Article
from ..database.db import get_boards_by_names
from ..modules.ai_summarizer import (
    summarize_and_save_to_db,
    summarize_and_save_to_db_ws,
)

router = APIRouter()


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

        # 동시에 3개의 작업까지 가능하게 제한함 (limit concurrency)
        semaphore = asyncio.Semaphore(3)

        async def limited_summary(article, db, websocket):
            async with semaphore:
                await summarize_and_save_to_db_ws(article, db, websocket)

        tasks = [
            limited_summary(article, db, websocket)
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

    # summarize_and_save_to_db_ws 호출 이전 과정에서 에러가 발생하면 아래에서 예외처리됨
    except ValueError as ve:
        await websocket.send_json(
            {"status": "error", "message": f"[서버 메시지] 입력 값 오류: {str(ve)}"}
        )
        await websocket.close()

    except Exception as e:
        await websocket.send_json(
            {"status": "error", "message": f"[서버 메시지] [⚠️ 서버 오류] {str(e)}"}
        )
        await websocket.close()


@router.get("/summarize_article/{article_id}")
async def summarize(article_id: int, db: Session = Depends(get_db)):
    try:
        article = db.get(Article, article_id)
        await summarize_and_save_to_db(article, db)

        return {"message": f"[서버 메시지] '{article.title}' 게시물을 요약 완료함"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"[⚠️ 서버 오류] '{article.title}' 게시물에서 오류 발생: {str(e)}",
        )
