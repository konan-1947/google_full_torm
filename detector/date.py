from bs4 import BeautifulSoup


def is_date(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Chọn ngày (Date, Loại 9) hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Chọn ngày, False nếu không.
    """
    try:
        # Phân tích chuỗi HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm thẻ <input type='date'>
        date_input = soup.find('input', attrs={'type': 'date'})
        if not date_input:
            return False

        # Tìm container cha gần nhất (div hoặc form)
        question_container = date_input.find_parent(['div', 'form'])
        if not question_container:
            return False

        # Kiểm tra nhãn ngày (tùy chọn, để tăng độ chính xác)
        label = question_container.find('div', class_='ds3H7c')
        if not label:
            # Nếu không có nhãn rõ ràng, vẫn chấp nhận nếu có input type='date'
            pass

        # Loại trừ các loại câu hỏi khác
        if (question_container.find('div', attrs={'role': 'radio'}) or
            question_container.find('div', attrs={'role': 'checkbox'}) or
            question_container.find('div', attrs={'role': 'listbox'}) or
            question_container.find('select') or
            question_container.find('textarea') or
            question_container.find('input', attrs={'type': 'file'}) or
            question_container.find('input', attrs={'type': 'time'}) or
                question_container.find('input', attrs={'type': 'text'})):
            return False

        return True

    except Exception as e:
        print(f"Lỗi khi phân tích HTML: {str(e)}")
        return False
