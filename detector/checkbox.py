from bs4 import BeautifulSoup


def is_checkbox(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Checkbox (Loại 4) hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Loại 4, False nếu không.
    """
    try:
        # Phân tích chuỗi HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm ít nhất một thẻ <div role='checkbox'>
        checkbox_options = soup.find_all('div', attrs={'role': 'checkbox'})
        if not checkbox_options:
            return False

        # Tìm container cha gần nhất của một checkbox (div hoặc form) để giới hạn phạm vi kiểm tra
        question_container = checkbox_options[0].find_parent(['div', 'form'])
        if not question_container:
            return False

        # Loại trừ các loại câu hỏi khác
        if (question_container.find('div', attrs={'role': 'radiogroup'}) or
            question_container.find('div', attrs={'role': 'listbox'}) or
            question_container.find('select') or
            question_container.find('textarea') or
            question_container.find('input', attrs={'type': 'file'}) or
            question_container.find('input', attrs={'type': 'date'}) or
                question_container.find('input', attrs={'type': 'time'})):
            return False

        return True

    except Exception as e:
        print(f"Lỗi khi phân tích HTML: {str(e)}")
        return False
