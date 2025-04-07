import requests
from bs4 import BeautifulSoup
from models import Board, Article
from config import db

# 유틸리티 함수들#####################################
# BeautifulSoup를 위한 함수 1
def fetch_html(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # raises if status is not 2xx/3xx
        return response.text
    except requests.RequestException as e:
        print(f"!!!Error fetching {url}: {e}")
        return None

# BeautifulSoup를 위한 함수 2
def make_soup(url):
    html = fetch_html(url)
    return BeautifulSoup(html, 'html.parser')

# 정확하게 해당 문자열만 뒤에서 지워주는 함수
# def rstrip_exact(s, suffix):
#     if suffix and s.endswith(suffix):
#         return s[:-len(suffix)]
#     return s

def rstrip_from(s, suffix):
    try:
        i = s.index(suffix)
        return s[:i]
    except:
        return s

def isInDateRange(date:str, date_range: tuple[str, str]):
    start_date, end_date = date_range
    return start_date <= date <= end_date

# 순서유지, 중복제거, None 제거
def clean_list(input_list):
    seen = set()
    return [x for x in input_list if x is not None and not (x.title in seen or seen.add(x.title                                                                             ))]

#########################################################################


# 게시글 하나의 날짜, 제목, 링크를 스크래핑하는 함수
def scrape_article(article_html, board, date_range):
    article_contents = article_html.find_all('td')

    pinned = 'top-notice-bg' in article_html.get('class', [])
    date = article_contents[-1].text

    if (pinned == True or isInDateRange(date, date_range)):
        title = article_contents[1].find('a').text
        link = rstrip_from(board.link + article_contents[1].find('a')['href'],"&article.offset=")

        return Article(pinned=pinned, date=date, title=title, link=link, board_id=board.id)
    
    # 고정 게시물도 아니고, 날짜 범위 안에도 들지 않는 경우
    return None

# 게시판 하나 안의 게시글들을 스크래핑하는 함수
def scrape_board(board_info, date_range):
    board_name, board_link = board_info

    # board_info를 바탕으로 새로운 Board 객체를 생성해서 DB에 추가
    # board = Board(name=board_name, link=board_link)
    # db.session.add(board)
    # db.session.flush()  # Ensure the board ID is generated for the relationship

    # DB에 이미 정의되어 있는 Board 객체 중 이름이 같은 것을 가져옴
    board = Board.query.filter_by(name=board_name).first()
    if not board:
        print(f"Board '{board_name}' not found in DB. Skipping.")
        return
    else:
        print(f"found Board '{board_name}' in DB.")

    articles = []
    for i in (0, 10):
        soup = make_soup(board.link + f"?mode=list&&articleLimit=10&article.offset={i}")
        if soup is None: # fetch_html에서 에러가 나면 None을 리턴함 -> make_soup에서 None을 리턴함 -> 이 경우는 스킵함
            print(f"Skipping offset {i} due to fetch failure.")
            continue
        else:
            print(f"Fetched offset {i} of {board.name} successfully.")

        articles_html = soup.find("tbody").find_all("tr")
        articles_sub = [scrape_article(article_html, board, date_range) for article_html in articles_html]
        articles.extend(articles_sub)
        print(f"Fetched {len(articles_sub)} articles from offset {i} of {board.name}.")

    valid_articles = clean_list(articles)
    print(f"Fetched {len(valid_articles)} valid articles from {board.name}.")

    db.session.add_all(valid_articles)
    db.session.commit()
    
def scrape_boards(board_infos, date_range):
    for board_info in board_infos:
        scrape_board(board_info, date_range)