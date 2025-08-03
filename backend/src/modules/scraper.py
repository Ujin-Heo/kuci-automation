import requests
import httpx
from fastapi import WebSocket
from bs4 import BeautifulSoup, Tag
from sqlalchemy.orm import Session

from ..database.models import Board, Article
from ..database.db import get_board_by_name


# 유틸리티 함수들#####################################
# BeautifulSoup를 위한 함수 1
def fetch_html(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises if status is not 2xx/3xx
        return response.text  # body of the response decoded as string form
    except requests.RequestException as e:
        print(f"다음 주소를 불러오는 데 실패함: {url} <-- {e}")
        return None


# BeautifulSoup를 위한 함수 2
def make_soup(url: str) -> BeautifulSoup | None:
    html = fetch_html(url)
    return BeautifulSoup(html, "html.parser")


# 비동기 BeautifulSoup 생성 함수 (TODO: 예외처리 추가하기)
async def make_soup_async(url: str) -> BeautifulSoup | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
    except httpx.RequestError as e:
        print(f"다음 주소를 비동기로 불러오는 데 실패함: {url} <-- {e}")
        return None


# 접미사 제거하는 함수
def rstrip_from(s: str, suffix: str) -> str:
    try:
        i = s.index(suffix)
        return s[:i]
    except:
        return s


# 날짜 범위 안에 들어오는지 확인하는 함수
def isInDateRange(date: str, date_range: tuple[str, str]) -> bool:
    start_date, end_date = date_range
    return start_date <= date <= end_date


# 순서유지, 중복제거, None 제거
def clean_list(input_list: list) -> list:
    seen = set()
    return [
        x
        for x in input_list
        if x is not None and not (x.title in seen or seen.add(x.title))
    ]


#########################################################################


# 게시글 하나의 날짜, 제목, 링크를 스크래핑하는 함수
def scrape_article(
    article_html: Tag, board: Board, date_range: tuple[str, str]
) -> Article | None:
    article_contents = article_html.find_all("td")

    pinned = "top-notice-bg" in article_html.get("class", [])
    date = article_contents[-1].text

    if pinned == True or isInDateRange(date, date_range):
        title = article_contents[1].find("a").text
        link = rstrip_from(
            board.link + article_contents[1].find("a")["href"], "&article.offset="
        )

        return Article(
            pinned=pinned, date=date, title=title, link=link, board_id=board.id
        )

    # 고정 게시물도 아니고, 날짜 범위 안에도 들지 않는 경우
    return None


# 게시판 하나 안의 게시글들을 스크래핑하는 함수
async def scrape_board(
    board_info: tuple[str, str],
    date_range: tuple[str, str],
    db: Session,
    websocket: WebSocket,
):
    board_name, _ = board_info  # _ is board_link
    try:
        # DB에 이미 정의되어 있는 Board 객체 중 이름이 같은 것을 가져옴
        board = get_board_by_name(db, board_name)
        if not board:
            print(f"Board '{board_name}' not found in DB. Skipping.")
            return
        else:
            print(f"found Board '{board_name}' in DB.")

        articles = []
        for i in (0, 10):
            soup = await make_soup_async(
                board.link + f"?mode=list&&articleLimit=10&article.offset={i}"
            )
            if (
                soup is None
            ):  # fetch_html에서 에러가 나면 None을 리턴함 -> make_soup에서 None을 리턴함 -> 이 경우는 스킵함
                print(f"Skipping offset {i} due to fetch failure.")
                continue
            else:
                print(f"Fetched offset {i} of {board.name} successfully.")

            articles_html = soup.find("tbody").find_all("tr")
            articles_sub = [
                scrape_article(article_html, board, date_range)
                for article_html in articles_html
            ]
            articles.extend(articles_sub)
            print(
                f"Fetched {len(articles_sub)} articles from offset {i} of {board.name}."
            )

        valid_articles = clean_list(articles)
        print(f"Fetched {len(valid_articles)} valid articles from {board.name}.")

        db.add_all(valid_articles)
        db.commit()

        await websocket.send_json(
            {
                "board": board_name,
                "status": "success",
                "message": f"[서버 메시지] '{board_name}' 게시판을 스크래핑 완료함",
            }
        )

    except Exception as e:
        print(f"Error scraping board '{board_name}': {e}")
        await websocket.send_json(
            {
                "board": board_name,
                "status": "error",
                "message": f"[서버 메시지] '{board_name}' 게시판에서 오류 발생: {str(e)}",
            }
        )


def scrape_boards(
    db: Session, board_infos: tuple[tuple[str, str], ...], date_range: tuple[str, str]
):
    for board_info in board_infos:
        scrape_board(board_info, date_range, db)
