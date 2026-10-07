# Sổ điểm lớp học - Bài tập tổng hợp Chương 3

## Chạy ứng dụng

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app sodiem run --debug --port 8000
```

## 1. Kết quả `flask --app sodiem routes`

```
...dán 10 dòng kết quả vào đây...
```

## 2. Kết quả các lệnh curl

```
...dán toàn bộ nội dung ketqua.txt vào đây...
```

## 3. Trả lời câu hỏi

**Vì sao dùng được `request` trong hàm xử lý lỗi dù nó không phải view function?**

`request` là một biến theo ngữ cảnh (context-local proxy). Khi có yêu cầu đến, Flask nạp request context trước khi điều phối đến view. Hàm xử lý lỗi cũng được gọi bên trong vòng đời của chính yêu cầu đó, nên request context vẫn còn hiệu lực và `request.path` trả về đúng yêu cầu đang xử lý. Điều kiện để dùng `request` là đang ở trong request context, không phụ thuộc hàm có được gắn `@app.route` hay không.

**Vì sao Câu 4 dùng 301 còn Câu 8 trả 201 kèm `Location`?**

301 Moved Permanently nghĩa là tài nguyên đã chuyển vĩnh viễn sang địa chỉ khác. Link rút gọn `/sv/<mssv>` chỉ là bí danh của `/students/<mssv>`, nên client được bảo đi theo `Location` và ghi nhớ lại. 201 Created nghĩa là yêu cầu PUT đã tạo ra một tài nguyên mới. Header `Location` lúc này chỉ cho client biết địa chỉ của tài nguyên vừa tạo, không có ý bảo client chuyển đi nơi khác.

**Thêm điểm cho 23T1020005 rồi khởi động lại server, điểm đó còn không? Vì sao?**

Không còn. Dữ liệu nằm trong dict `STUDENTS`, tức là trong bộ nhớ của tiến trình Python. Điểm thêm vào chỉ thay đổi dict trong tiến trình đang chạy. Khi server khởi động lại, mã nguồn được nạp lại và `STUDENTS` trở về giá trị khai báo ban đầu. Muốn giữ điểm thì phải lưu ra file hoặc cơ sở dữ liệu.cd 