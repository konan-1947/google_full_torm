from bs4 import BeautifulSoup
import os
import json


def detect_google_form_questions(html_file_path, output_json_path="form_analysis.json"):
    """
    Hàm quét file HTML của Google Forms, phát hiện các câu hỏi, loại câu trả lời, các lựa chọn,
    và xuất kết quả ra file JSON.

    Args:
        html_file_path (str): Đường dẫn đến file HTML cần phân tích.
        output_json_path (str): Đường dẫn đến file JSON để lưu kết quả.
    """
    # Kiểm tra file HTML có tồn tại không
    if not os.path.exists(html_file_path):
        print(f"Không tìm thấy file: {html_file_path}")
        return

    try:
        # Đọc nội dung file HTML
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Tạo đối tượng BeautifulSoup để phân tích HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm tất cả các section câu hỏi (thường là div class="geS5n")
        question_sections = soup.find_all('div', class_='geS5n')
        if not question_sections:
            print("Không tìm thấy câu hỏi nào trong file HTML.")
            return

        # Danh sách lưu kết quả
        results = []

        # Duyệt qua từng section câu hỏi
        for idx, section in enumerate(question_sections, 1):
            question_data = {
                "question_id": idx,
                "title": "",
                "answer_type": "Không xác định",
                "choices": []
            }

            # Lấy tiêu đề câu hỏi
            question_title = section.find('span', class_='M7eMe')
            question_data["title"] = question_title.get_text(
                strip=True) if question_title else "Không có tiêu đề"

            # Xác định loại câu trả lời
            # 1. Câu trả lời ngắn hoặc Đoạn văn
            if section.find('input', type='text'):
                question_data["answer_type"] = "Câu trả lời ngắn (Short answer)"
            elif section.find('textarea'):
                question_data["answer_type"] = "Đoạn văn (Paragraph)"

            # 2. Trắc nghiệm hoặc Thang đo tuyến tính
            elif section.find('div', role='radiogroup'):
                radiogroups = section.find_all('div', role='radiogroup')
                if len(radiogroups) > 1 or section.find('div', class_='ssX1Bd'):  # Lưới trắc nghiệm
                    question_data["answer_type"] = "Lưới trắc nghiệm (Multiple Choice Grid)"
                    # Lấy các cột (lựa chọn)
                    headers = section.find('div', class_='ssX1Bd KZt9Tc')
                    if headers:
                        header_texts = [header.get_text(strip=True) for header in headers.find_all(
                            'div', class_='V4d7Ke OIC90c')]
                        question_data["choices"].append(
                            f"Các cột lựa chọn: {', '.join(header_texts)}")
                    # Lấy các hàng (câu hỏi con)
                    for row_idx, radiogroup in enumerate(radiogroups, 1):
                        row_label = radiogroup.find(
                            'div', class_='V4d7Ke wzWPxe OIC90c')
                        row_text = row_label.get_text(
                            strip=True) if row_label else f"Hàng {row_idx}"
                        entry_input = radiogroup.find('input', type='hidden')
                        entry_id = entry_input.get(
                            'name', 'Không có ID') if entry_input else 'Không có ID'
                        row_choices = [choice.get('data-value', 'Không xác định')
                                       for choice in radiogroup.find_all('div', role='radio')]
                        question_data["choices"].append(
                            f"Hàng {row_idx}: {row_text} (Entry ID: {entry_id}), Lựa chọn: {', '.join(row_choices)}"
                        )
                else:  # Trắc nghiệm hoặc Thang đo tuyến tính
                    radio_choices = section.find_all('div', role='radio')
                    choice_values = [choice.get(
                        'data-value', choice.get_text(strip=True)) for choice in radio_choices]
                    if all(val.isdigit() for val in choice_values if val):  # Thang đo tuyến tính
                        question_data["answer_type"] = "Thang đo tuyến tính (Linear scale)"
                    else:
                        question_data["answer_type"] = "Trắc nghiệm (Multiple choice)"
                    question_data["choices"] = choice_values

            # 3. Hộp kiểm
            elif section.find('div', role='checkbox'):
                question_data["answer_type"] = "Hộp kiểm (Checkboxes)"
                checkbox_choices = section.find_all('div', role='checkbox')
                question_data["choices"] = [choice.get(
                    'data-value', choice.get_text(strip=True)) for choice in checkbox_choices]

            # 4. Danh sách thả xuống
            elif section.find('div', role='listbox') or section.find('select'):
                question_data["answer_type"] = "Danh sách thả xuống (Dropdown)"
                options = section.find_all(
                    'div', role='option') or section.find_all('option')
                question_data["choices"] = [
                    option.get_text(strip=True) for option in options]

            # 5. Tải tệp lên
            elif section.find('input', type='file'):
                question_data["answer_type"] = "Tải tệp lên (File upload)"

            # 6. Ngày hoặc Thời gian
            elif section.find('input', type='date'):
                question_data["answer_type"] = "Ngày (Date)"
            elif section.find('input', type='time'):
                question_data["answer_type"] = "Thời gian (Time)"

            # 7. Lưới hộp kiểm
            elif section.find('div', class_='ssX1Bd') and section.find('div', role='checkbox'):
                question_data["answer_type"] = "Lưới hộp kiểm (Checkbox Grid)"
                headers = section.find('div', class_='ssX1Bd KZt9Tc')
                if headers:
                    header_texts = [header.get_text(strip=True) for header in headers.find_all(
                        'div', class_='V4d7Ke OIC90c')]
                    question_data["choices"].append(
                        f"Các cột lựa chọn: {', '.join(header_texts)}")
                checkbox_groups = section.find_all('div', role='group')
                for row_idx, group in enumerate(checkbox_groups, 1):
                    row_label = group.find(
                        'div', class_='V4d7Ke wzWPxe OIC90c')
                    row_text = row_label.get_text(
                        strip=True) if row_label else f"Hàng {row_idx}"
                    row_choices = [choice.get('data-value', 'Không xác định')
                                   for choice in group.find_all('div', role='checkbox')]
                    question_data["choices"].append(
                        f"Hàng {row_idx}: {row_text}, Lựa chọn: {', '.join(row_choices)}"
                    )

            # Thêm dữ liệu câu hỏi vào kết quả
            results.append(question_data)

        # Xuất kết quả ra file JSON
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)
        print(f"Kết quả đã được lưu vào: {output_json_path}")

    except Exception as e:
        print(f"Đã xảy ra lỗi khi phân tích file HTML: {str(e)}")


# Ví dụ sử dụng
if __name__ == "__main__":
    # Thay đường dẫn này bằng file HTML của cậu
    html_file = "sample.html"
    detect_google_form_questions(html_file, "form_analysis.json")
