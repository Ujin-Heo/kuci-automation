from pptx import Presentation
from pptx.util import Pt
from models import Board
import os

def chunk_list(my_list, chunk_size=4):
    return [my_list[i:i+chunk_size] for i in range(0, len(my_list), chunk_size)]

def select_shape_by_text(slide, text):
    shapes = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                if text in paragraph.text:
                    shapes.append(shape)
    return shapes

def write_slide(slide, articles):
    shapes = select_shape_by_text(slide, "제목")
    for shape, article in zip(shapes, articles):
        text_frame = shape.text_frame
        new_text = article.title
        
        text_frame.auto_size = False
        max_width = shape.width
        text_frame.paragraphs[0].runs[0].text = new_text
        font_size = Pt(108)  # Set a reasonable starting font size

        # Adjust font size to fit
        while text_frame.text and text_frame.width > max_width:
            font_size -= Pt(12)  # Decrease font size gradually
            text_frame.paragraphs[0].runs[0].font.size = font_size
            
    return
        

def make_ppt(month, week, writer, template_path='template.pptx'):
    template_path = os.path.join(os.path.dirname(__file__), template_path)
    print(template_path)
    prs = Presentation(template_path)

    title_page = prs.slides[0]
    date_shape = select_shape_by_text(title_page, 'n월 m주차')[0]
    date_shape.text = f"2024년 {month}월 {week}주차"
    author_shape = select_shape_by_text(title_page, "담당자")[0]
    author_shape.text_frame.paragraphs[0].runs[0].text = f": 교육진로국원 {writer}"

    template_page = prs.slides[1]

    ppt_sectors = {
        '일반공지': Board.query.filter_by(name='공지사항').first().articles,
        '행사 및 공모전': Board.query.filter_by(name='행사 및 소식').first().articles + Board.query.filter_by(name='진로정보(공모전)').first().articles,
        '채용 및 인턴 모집': Board.query.filter_by(name='진로정보(채용)').first().articles + Board.query.filter_by(name='진로정보(인턴)').first().articles,
        '전공 관련 교육행사': Board.query.filter_by(name='진로정보(교육)').first().articles
    }

    for sector_title, articles in ppt_sectors.items():
        article_chunks = chunk_list(articles)
 
        for article_chunk in article_chunks:
            slide = prs.slides.add_slide(template_page.slide_layout)  # Duplicate the template slide
            slide_title = select_shape_by_text(slide, "슬라이드")
            slide_title.text_frame.paragraphs[0].runs[0].text = sector_title
            write_slide(slide, article_chunk)

    # Save the modified presentation
    prs.save(f"{month}월_{week}주차_전공소식공유.pptx")

if __name__ == "__main__":
    template_path='template.pptx'
    template_path = os.path.join(os.path.dirname(__file__), template_path)
    print(template_path)