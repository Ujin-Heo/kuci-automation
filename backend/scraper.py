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
def rstrip_exact(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s
#########################################################################


# 게시글 하나의 날짜, 제목, 링크를 스크래핑하는 함수
def scrape_article(article_html, board):
    article_contents = article_html.find_all('td')

    date = article_contents[-1].text
    title = article_contents[1].find('a').text
    link = rstrip_exact(board.link + article_contents[1].find('a')['href'],"&article.offset=0&articleLimit=10&totalNoticeYn=N&totalBoardNo=")

    return Article(date, title, link, board)

# 게시판 하나 안의 게시글들을 스크래핑하는 함수
def scrape_board(board_info):
    board = Board(*board_info)
    db.session.add(board)

    soup = make_soup(board.link)
    articles_html = soup.find("tbody").find_all("tr")

    articles = [scrape_article(article_html, board) for article_html in articles_html]
    db.session.add_all(articles)

    db.session.commit()
    

def scrape_boards(board_infos):
    for board_info in board_infos.values():
        scrape_board(board_info)