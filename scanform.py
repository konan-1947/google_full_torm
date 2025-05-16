import json
from bs4 import BeautifulSoup

# Giả sử hàm detect_question_type đã được nhập
from detector.detect_question_type import detect_question_type


def scan_form(html_file, output_json):
    """
    Quét file HTML của Google Form để xác định loại câu hỏi, tiêu đề, và thông tin đáp án.
    Lưu kết quả vào file JSON để sử dụng với Selenium.

    Args:
        html_file (str): Đường dẫn đến file HTML (sample.html).
        output_json (str): Đường dẫn đến file JSON đầu ra (results.json).

    Returns:
        bool: True nếu quét và lưu thành công, False nếu thất bại.
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        question_elements = soup.find_all(
            'div', class_='Qr7Oae', attrs={'role': 'listitem'})
        if not question_elements:
            print("Lỗi: Không tìm thấy câu hỏi nào trong file HTML.")
            return False

        results = []

        for index, question_element in enumerate(question_elements):
            question_html = str(question_element)
            question_type = detect_question_type(question_html)
            if question_type == "Unknown":
                print(
                    f"Cảnh báo: Không xác định được loại câu hỏi {index + 1}.")
                results.append({"index": index, "type": "Unknown",
                               "title": "", "answer_format": "unknown"})
                continue

            title_element = question_element.find('span', class_='M7eMe')
            title = title_element.text.strip(
            ) if title_element and title_element.text.strip() else "Không có tiêu đề"

            question_info = {
                "index": index,
                "type": question_type,
                "title": title,
                "answer_format": ""
            }

            if question_type == "Short Answer":
                question_info["answer_format"] = "text"

            elif question_type == "Paragraph Answer":
                question_info["answer_format"] = "long_text"

            elif question_type == "Multiple Choice":
                question_info["answer_format"] = "single_choice"
                options = []
                choice_elements = question_element.find_all(
                    'div', class_='nWQGrd zwllIb')
                for choice in choice_elements:
                    label = choice.find('span', class_='aDTYNe')
                    if label and label.text.strip() and label.text.strip() != "Mục khác:":
                        options.append(label.text.strip())
                    elif choice.find('div', class_='pIDwKe'):  # Kiểm tra "Mục khác:"
                        options.append("Mục khác:")
                question_info["options"] = options if options else [
                    "Tùy chọn không xác định"]

            elif question_type == "Checkbox":
                question_info["answer_format"] = "multiple_choice"
                options = []
                checkbox_elements = question_element.find_all(
                    'div', class_='eBFwI')
                for checkbox in checkbox_elements:
                    label = checkbox.find('span', class_='aDTYNe')
                    if label and label.text.strip() and label.text.strip() != "Mục khác:":
                        options.append(label.text.strip())
                    elif checkbox.find('div', class_='xVfcde'):  # Kiểm tra "Mục khác:"
                        options.append("Mục khác:")
                question_info["options"] = options if options else [
                    "Tùy chọn không xác định"]

            elif question_type == "Dropdown":
                question_info["answer_format"] = "single_choice"
                options = []
                dropdown_elements = question_element.find_all(
                    'div', class_='MocG8c', attrs={'role': 'option'})
                for option in dropdown_elements:
                    text = option.find('span', class_='vRMGwf')
                    if text and text.text.strip() and text.text.strip() != "Chọn":
                        options.append(text.text.strip())
                question_info["options"] = options if options else [
                    "Tùy chọn không xác định"]

            elif question_type == "File Upload":
                question_info["answer_format"] = "file"
                constraints = {"max_files": 1, "max_size": "10MB"}
                description = question_element.find('div', class_='Y01Dsf')
                if description:
                    text = description.text.lower()
                    if "kích thước tối đa" in text:
                        size_part = text.split("kích thước tối đa")[
                            1].split('.')[0].strip()
                        constraints["max_size"] = size_part
                    if "tải" in text and "tệp" in text:
                        num_files = text.split("tải")[1].split("tệp")[
                            0].strip()
                        constraints["max_files"] = int(
                            num_files) if num_files.isdigit() else 1
                question_info["constraints"] = constraints

            elif question_type == "Linear Scale":
                question_info["answer_format"] = "scale"
                scale_elements = question_element.find_all(
                    'div', class_='Zki2Ve')
                values = [int(elem.text.strip())
                          for elem in scale_elements if elem.text.strip().isdigit()]
                if values:
                    question_info["range"] = {
                        "min": min(values), "max": max(values)}
                else:
                    question_info["range"] = {"min": 1, "max": 10}

            elif question_type == "Star Rating":
                question_info["answer_format"] = "star"
                scale_elements = question_element.find_all(
                    'div', class_='Zki2Ve')
                values = [int(elem.text.strip())
                          for elem in scale_elements if elem.text.strip().isdigit()]
                if values:
                    question_info["range"] = {
                        "min": min(values), "max": max(values)}
                else:
                    question_info["range"] = {"min": 1, "max": 10}

            elif question_type == "Multiple Choice Grid":
                question_info["answer_format"] = "grid_single_choice"
                rows = [row.text.strip() for row in question_element.find_all(
                    'div', class_='V4d7Ke wzWPxe OIC90c')]
                columns = [col.text.strip() for col in question_element.select(
                    '.ssX1Bd.KZt9Tc .V4d7Ke.OIC90c')]
                question_info["rows"] = rows if rows else [
                    "Hàng không xác định"]
                question_info["columns"] = columns if columns else [
                    "Cột không xác định"]

            elif question_type == "Checkbox Grid":
                question_info["answer_format"] = "grid_multiple_choice"
                rows = [row.text.strip() for row in question_element.find_all(
                    'div', class_='V4d7Ke wzWPxe OIC90c')]
                columns = [col.text.strip() for col in question_element.select(
                    '.ssX1Bd.KZt9Tc .V4d7Ke.OIC90c')]
                question_info["rows"] = rows if rows else [
                    "Hàng không xác định"]
                question_info["columns"] = columns if columns else [
                    "Cột không xác định"]

            elif question_type == "Date":
                question_info["answer_format"] = "date"

            elif question_type == "Time":
                question_info["answer_format"] = "time"

            results.append(question_info)

        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print(
            f"Đã lưu kết quả phân tích vào {output_json} với {len(results)} câu hỏi.")
        return True

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {html_file}.")
        return False
    except Exception as e:
        print(f"Lỗi khi quét file HTML: {str(e)}")
        return False
