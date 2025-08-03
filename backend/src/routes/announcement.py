from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from ..database.models import get_db
from ..modules.writer import write_announcement


class AnnouncementMetaData(BaseModel):
    month: str
    week: str
    writer: str


router = APIRouter()


# 공지글 작성하기
@router.post("/announcement")
async def announcement(
    metadata: AnnouncementMetaData,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        month = metadata.month
        week = metadata.week
        writer = metadata.writer

        file_path = write_announcement(db, month, week, writer)

        # 프론트엔드로 파일 보낸 후 벡엔드 서버에서는 삭제
        background_tasks.add_task(remove_file_safe, file_path)

        # Send the file
        return FileResponse(
            file_path,
            media_type="text/plain",
            # filename=os.path.basename(file_path) -> 이렇게 하면 다운로드될 파일 이름 백엔드에서 지정 가능
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"[서버 메시지] [⚠️ 서버 오류] {str(e)}"
        )


def remove_file_safe(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Error removing file {path}: {e}")
