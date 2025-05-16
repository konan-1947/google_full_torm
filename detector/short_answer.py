from bs4 import BeautifulSoup


def is_short_answer(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Câu trả lời ngắn (Loại 1) hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Loại 1, False nếu không.
    """
    try:
        # Phân tích chuỗi HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm thẻ <input> với type='text'
        input_text = soup.find('input', type='text')
        if not input_text:
            return False

        # Tìm container cha gần nhất của input (div hoặc form) để giới hạn phạm vi kiểm tra
        question_container = input_text.find_parent(['div', 'form'])
        if not question_container:
            return False

        # Loại trừ các loại câu hỏi khác
        if (question_container.find('div', role='radiogroup') or
            question_container.find('div', role='checkbox') or
            question_container.find('div', role='listbox') or
            question_container.find('select') or
            question_container.find('textarea') or
            question_container.find('input', type='file') or
            question_container.find('input', type='date') or
                question_container.find('input', type='time')):
            return False

        return True

    except Exception as e:
        print(f"Lỗi khi phân tích HTML: {str(e)}")
        return False
