import requests
from bs4 import BeautifulSoup
from models import Board, Article
from config import db

# 유틸리티 함수들#####################################
# BeautifulSoup를 위한 함수 1
def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch the URL: {url}, Status code: {response.status_code}")

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
    # board = Board(*board_info)
    # db.session.add(board)

    board_name, board_link = board_info
    board = Board(name=board_name, link=board_link)
    db.session.add(board)
    db.session.flush()  # Ensure the board ID is generated for the relationship
    
    articles = []
    for i in (0, 10):
        soup = make_soup(board.link + f"?mode=list&&articleLimit=10&article.offset={i}")
        articles_html = soup.find("tbody").find_all("tr")
        articles_sub = [scrape_article(article_html, board, date_range) for article_html in articles_html]
        articles.extend(articles_sub)

    valid_articles = clean_list(articles)

    db.session.add_all(valid_articles)
    db.session.commit()
    
def scrape_boards(board_infos, date_range):
    for board_info in board_infos:
        scrape_board(board_info, date_range)