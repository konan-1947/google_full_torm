from bs4 import BeautifulSoup


def is_linear_scale(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Thang đo tuyến tính (Loại 7) hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Loại 7, False nếu không.
    """
    try:
        # Phân tích chuỗi HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm thẻ <div role='radiogroup'>
        radiogroup = soup.find('div', attrs={'role': 'radiogroup'})
        if not radiogroup:
            return False

        # Tìm container cha gần nhất của radiogroup (div hoặc form) để giới hạn phạm vi kiểm tra
        question_container = radiogroup.find_parent(['div', 'form'])
        if not question_container:
            return False

        # Kiểm tra các tùy chọn radio
        radio_options = radiogroup.find_all('div', attrs={'role': 'radio'})
        if not radio_options:
            return False

        # Kiểm tra xem các tùy chọn có phải là số liên tiếp
        values = []
        for option in radio_options:
            value = option.get('data-value', '')
            if value.isdigit():
                values.append(int(value))

        if not values:
            return False

        # Kiểm tra tính liên tiếp của các giá trị (tăng dần, không có khoảng trống)
        sorted_values = sorted(values)
        if sorted_values != list(range(min(sorted_values), max(sorted_values) + 1)):
            return False

        # Loại trừ các loại câu hỏi khác
        if (question_container.find('div', attrs={'role': 'checkbox'}) or
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
