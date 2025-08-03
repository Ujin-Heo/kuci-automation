from fastapi import WebSocket, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

from ..database.models import Article
from .scraper import make_soup_async


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

user_prompt_instructions = f"""# Instructions
Extract key information from the given Korean announcement.
The key information to extract are "subject, registration period or deadline, event period or date, venue, registration guide"
Extract the information in Korean.
If there is no information to extract for a key information, put "not found".

Return the extracted information in the following JSON structure.
Keep the key names exactly same as the format below, and make sure the values are string in Korean or "not found".
# Format
{{
        "subject": "Description of the event in phrases",
        "registrationPeriodOrDeadline": "yyyy. mm. dd.(요일) - mm. dd. (요일) for period / yyyy. mm. dd. (요일)까지 for deadline + put time in 24hr formmat if mentioned",
        "eventPeriodOrDate": "yyyy. mm. dd.(요일) - mm. dd. (요일) for period / yyyy. mm. dd. (요일) for a single date + put time in 24hr formmat if mentioned",
        "venue": "venue of the event",
        "registrationGuide": "Simple guide on how to apply or registration link",
}}
"""


async def summarize_with_ai(article_content: str) -> dict[str, Any]:

    system_instruction_content = types.Content(
        parts=[
            types.Part(text="You are an expert announcement summarizer."),
            # You can add more parts here if your system instruction is multimodal
        ]
    )

    user_prompt_content = types.Content(
        role="user",
        parts=[
            types.Part(text=user_prompt_instructions),
            types.Part(text=f"# Given announcement to summarize\n{article_content}"),
        ],
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[user_prompt_content],
            config=types.GenerateContentConfig(
                temperature=0.5,
                response_mime_type="application/json",
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                system_instruction=system_instruction_content,
            ),
        )

        content = response.text
        print("------------------------------------------------------------\n")
        print(content)
        print("------------------------------------------------------------\n")
        summary_data = json.loads(content)

        required_fields = (
            "subject",
            "registrationPeriodOrDeadline",
            "eventPeriodOrDate",
            "venue",
            "registrationGuide",
        )
        for field in required_fields:
            if field not in summary_data:
                raise ValueError(f"Missing required field: {field}")

        return summary_data

    except Exception as e:
        print(f"Error summarizing article: {e}")
        return {
            "subject": "not found(오류 발생)",
            "registrationPeriodOrDeadline": "not found(오류 발생)",
            "eventPeriodOrDate": "not found(오류 발생)",
            "venue": "not found(오류 발생)",
            "registrationGuide": "not found(오류 발생)",
        }


async def summarize_and_save_to_db_ws(
    article: Article, db: Session, websocket: WebSocket
):
    try:
        article_soup = await make_soup_async(article.link)
        content_tags = (
            article_soup.select(".article-text")[0]
            .select(".fr-view")[0]
            .find_all(["div", "p"])
        )
        article_content = "".join(
            f"{tag.text}\n" for tag in content_tags if tag.text != ""
        )
        summary_data: dict = await summarize_with_ai(article_content)

        article.content = summary_data
        db.commit()

        await websocket.send_json(
            {
                "article": article.title,
                "status": "success",
                "message": f"[서버 메시지] '{article.title}' 게시물을 요약 완료함",
            }
        )

    except Exception as e:
        print(f"Error summarizing article {article.title}: {e}")
        await websocket.send_json(
            {
                "article": article.title,
                "status": "error",
                "message": f"[⚠️ 서버 오류] '{article.title}' 게시물에서 오류 발생: {str(e)}",
            }
        )


async def summarize_and_save_to_db(article: Article, db: Session):
    try:
        article_soup = await make_soup_async(article.link)
        content_tags = (
            article_soup.select(".article-text")[0]
            .select(".fr-view")[0]
            .find_all(["div", "p"])
        )
        article_content = "".join(
            f"{tag.text}\n" for tag in content_tags if tag.text != ""
        )
        summary_data: dict = await summarize_with_ai(article_content)

        article.content = summary_data
        db.commit()

    except Exception as e:
        print(f"Error summarizing article {article.title}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"[⚠️ 서버 오류] '{article.title}' 게시물에서 오류 발생: {str(e)}",
        )
