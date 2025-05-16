# các thứ đã làm đc: 

## khi chạy app.py bây giờ: 
- chạy file scan_form để quét file html (trong thư mục input)
- Quét file HTML của Google Form để xác định loại câu hỏi, tiêu đề, và thông tin đáp án (form tổng trong trang form)
- Xuất ra kết quả ra file JSON tại thư mục output

## những gì đang cần làm thêm
- với mỗi form đã có sẵn thể loại (đã đc detect) thì có hàm selenium để điền tự động
- mỗi hàm đó sẽ có tham số vào là số lượng, tỉ lệ custom (nếu có - làm sau)
- đây mới chỉ là làm với 1 page, form có nhiều page sẽ tính sau

## đã có đầy đủ các form của gg form, sau này có cập nhật thì chỉ cần sửa hàm