from bs4 import BeautifulSoup
from detector import (
    is_date,
    is_time,
    is_file_upload,
    is_multiple_choice_grid,
    is_checkbox_grid,
    is_dropdown,
    is_star_rating,
    is_linear_scale,
    is_multiple_choice,
    is_checkbox,
    is_short_answer,
    is_paragraph_answer,
)


def detect_question_type(html_content):
    """
    Xác định loại câu hỏi Google Forms từ đoạn HTML.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        str: Tên loại câu hỏi (hoặc 'Unknown' nếu không xác định được).
    """
    try:
        # Phân tích chuỗi HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Kiểm tra các loại câu hỏi theo thứ tự ưu tiên mới
        if is_date(html_content):
            return "Date"
        elif is_time(html_content):
            return "Time"
        elif is_file_upload(html_content):
            return "File Upload"
        elif is_multiple_choice_grid(html_content):
            return "Multiple Choice Grid"
        elif is_checkbox_grid(html_content):
            return "Checkbox Grid"
        elif is_dropdown(html_content):
            return "Dropdown"
        elif is_star_rating(html_content):
            return "Star Rating"
        elif is_linear_scale(html_content):
            return "Linear Scale"
        elif is_multiple_choice(html_content):
            return "Multiple Choice"
        elif is_checkbox(html_content):
            return "Checkbox"
        elif is_short_answer(html_content):
            return "Short Answer"
        elif is_paragraph_answer(html_content):
            return "Paragraph Answer"
        else:
            return "Unknown"

    except Exception as e:
        print(f"Lỗi khi phân tích HTML: {str(e)}")
        return "Unknown"
