from bs4 import BeautifulSoup


def is_dropdown(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Danh sách thả xuống (Loại 5) hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Loại 5, False nếu không.
    """
    try:
        # Phân tích chuỗi HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Tìm thẻ <div role='listbox'>
        listbox = soup.find('div', attrs={'role': 'listbox'})
        if not listbox:
            return False

        # Tìm container cha gần nhất của listbox (div hoặc form) để giới hạn phạm vi kiểm tra
        question_container = listbox.find_parent(['div', 'form'])
        if not question_container:
            return False

        # Kiểm tra sự hiện diện của ít nhất một tùy chọn option
        options = listbox.find_all('div', attrs={'role': 'option'})
        if not options:
            return False
        # Loại trừ các loại câu hỏi khác
        if (
            question_container.find('div', attrs={'role': 'radiogroup'}) or
            question_container.find('div', attrs={'role': 'checkbox'}) or
            question_container.find('select') or
            question_container.find('textarea') or
            question_container.find('input', attrs={'type': 'text'}) or
            question_container.find('input', attrs={'type': 'file'}) or
            question_container.find('input', attrs={'type': 'date'}) or
                question_container.find('input', attrs={'type': 'time'})):
            return False
        return True

    except Exception as e:
        print(f"Lỗi khi phân tích HTML: {str(e)}")
        return False
