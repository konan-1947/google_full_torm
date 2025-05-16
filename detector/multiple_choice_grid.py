from bs4 import BeautifulSoup


def is_multiple_choice_grid(html_content):
    """
    Kiểm tra xem đoạn HTML có chứa câu hỏi Multiple Choice Grid hay không.

    Args:
        html_content (str): Chuỗi HTML chứa một câu hỏi.

    Returns:
        bool: True nếu câu hỏi khớp với mẫu Multiple Choice Grid, False nếu không.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Kiểm tra số lượng radiogroup (ít nhất 2 hàng)
        radiogroups = soup.find_all('div', attrs={'role': 'radiogroup'})
        if len(radiogroups) > 1:
            return True

        # Kiểm tra sự hiện diện của các hàng (SG0AAe)
        rows = soup.find_all('div', class_='SG0AAe')
        if len(rows) > 1 and any(row.find('div', attrs={'role': 'radiogroup'}) for row in rows):
            return True

        return False

    except Exception:
        return False
