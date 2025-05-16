from bs4 import BeautifulSoup


def is_file_upload(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Tải tệp (File Upload, Loại 6) hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Tải tệp, False nếu không.
    """
    try:
        # Phân tích chuỗi HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm nút "Thêm tệp" (div role='button' với aria-label chứa "Thêm tệp" hoặc "Add file")
        upload_button = soup.find('div', attrs={
                                  'role': 'button', 'aria-label': lambda x: x and ('Thêm tệp' in x or 'Add file' in x)})
        if not upload_button:
            return False

        # Tìm container cha gần nhất (div hoặc form)
        question_container = upload_button.find_parent(['div', 'form'])
        if not question_container:
            return False

        # Kiểm tra mô tả giới hạn tệp (tùy chọn, để tăng độ chính xác)
        description = question_container.find('div', class_='Y01Dsf')
        if description and ('tệp' in description.text.lower() or 'file' in description.text.lower()):
            pass  # Tăng độ tin cậy, nhưng không bắt buộc

        # Loại trừ các loại câu hỏi khác
        if (question_container.find('div', attrs={'role': 'radio'}) or
            question_container.find('div', attrs={'role': 'checkbox'}) or
            question_container.find('div', attrs={'role': 'listbox'}) or
            question_container.find('select') or
            question_container.find('textarea') or
            question_container.find('input', attrs={'type': 'text'}) or
            question_container.find('input', attrs={'type': 'date'}) or
                question_container.find('input', attrs={'type': 'time'})):
            return False

        return True

    except Exception as e:
        print(f"Lỗi khi phân tích HTML: {str(e)}")
        return False
