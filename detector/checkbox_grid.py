from bs4 import BeautifulSoup


def is_checkbox_grid(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Lưới kiểm (Checkbox Grid, Loại 10) hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Loại 10, False nếu không.
    """
    try:
        # Phân tích chuỗi HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm tất cả các thẻ <div role='group'> đại diện cho các hàng
        groups = soup.find_all('div', attrs={'role': 'group'})
        if len(groups) < 2:
            return False

        # Tìm container cha gần nhất của group đầu tiên (div hoặc form)
        question_container = groups[0].find_parent(['div', 'form'])
        if not question_container:
            return False

        # Kiểm tra các tùy chọn checkbox trong mỗi group
        column_values = None
        for group in groups:
            checkbox_options = group.find_all(
                'div', attrs={'role': 'checkbox'})
            if not checkbox_options:
                return False

            # Lấy danh sách giá trị data-answer-value của các checkbox
            values = [option.get('data-answer-value', '')
                      for option in checkbox_options if option.get('data-answer-value')]
            if not values:
                return False

            # Kiểm tra xem các group có cùng danh sách tùy chọn cột
            if column_values is None:
                column_values = sorted(values)
            elif sorted(values) != column_values:
                return False

        # Kiểm tra sự hiện diện của nhãn cột
        column_labels = question_container.find('div', class_='ssX1Bd')
        if not column_labels or not column_labels.find_all('div', class_='V4d7Ke'):
            return False

        # Loại trừ các loại câu hỏi khác
        if (question_container.find('div', attrs={'role': 'radio'}) or
            question_container.find('div', attrs={'role': 'listbox'}) or
            question_container.find('select') or
            question_container.find('textarea') or
            question_container.find('input', attrs={'type': 'file'}) or
            question_container.find('input', attrs={'type': 'date'}) or
                question_container.find('input', attrs={'type': 'time'})):
            return False

        # Loại trừ Thang đo tuyến tính và Thang đánh giá sao
        checkbox_options = groups[0].find_all(
            'div', attrs={'role': 'checkbox'})
        values = [option.get('data-answer-value', '')
                  for option in checkbox_options if option.get('data-answer-value')]
        if all(value.isdigit() for value in values):
            int_values = [int(v) for v in values]
            sorted_values = sorted(int_values)
            if sorted_values == list(range(min(sorted_values), max(sorted_values) + 1)):
                return False

        return True

    except Exception as e:
        print(f"Lỗi khi phân tích HTML: {str(e)}")
        return False
