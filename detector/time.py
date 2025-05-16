from bs4 import BeautifulSoup


def is_time(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Chọn thời gian (Time, Loại 10) hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Chọn thời gian, False nếu không.
    """
    try:
        # Phân tích chuỗi HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm tất cả thẻ <input type='text'>
        text_inputs = soup.find_all('input', attrs={'type': 'text'})
        if len(text_inputs) < 2:
            return False

        # Kiểm tra xem có trường giờ và phút
        hour_input = None
        minute_input = None
        for input_tag in text_inputs:
            aria_label = input_tag.get('aria-label', '').lower()
            if 'giờ' in aria_label or 'hour' in aria_label:
                hour_input = input_tag
            elif 'phút' in aria_label or 'minute' in aria_label:
                minute_input = input_tag

        if not (hour_input and minute_input):
            return False

        # Kiểm tra thuộc tính đặc trưng của giờ và phút
        if (hour_input.get('maxlength') != '2' or
            hour_input.get('min') != '0' or
            hour_input.get('max') != '23' or
            minute_input.get('maxlength') != '2' or
            minute_input.get('min') != '0' or
                minute_input.get('max') != '59'):
            return False

        # Tìm container cha gần nhất (div hoặc form)
        question_container = hour_input.find_parent(['div', 'form'])
        if not question_container:
            return False

        # Kiểm tra dấu phân tách giữa giờ và phút
        separator = question_container.find('div', class_='IDmXx')
        if not separator or separator.text.strip() != ':':
            return False

        # Loại trừ các loại câu hỏi khác
        if (question_container.find('div', attrs={'role': 'radio'}) or
            question_container.find('div', attrs={'role': 'checkbox'}) or
            question_container.find('div', attrs={'role': 'listbox'}) or
            question_container.find('select') or
            question_container.find('textarea') or
            question_container.find('input', attrs={'type': 'file'}) or
                question_container.find('input', attrs={'type': 'date'})):
            return False

        return True

    except Exception as e:
        print(f"Lỗi khi phân tích HTML: {str(e)}")
        return False
