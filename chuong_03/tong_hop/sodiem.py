from flask import Flask, request, url_for
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A",
                   "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A",
                   "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B",
                   "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B",
                   "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A",
                   "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C",
                   "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}


def average(scores):
    """Trung bình cộng, làm tròn 2 chữ số; dict rỗng -> None."""
    if not scores:
        return None
    return round(sum(scores.values()) / len(scores), 2)


def rank(avg):
    if avg is None:
        return "Chưa có điểm"
    if avg >= 8.5:
        return "Giỏi"
    if avg >= 7.0:
        return "Khá"
    if avg >= 5.0:
        return "Trung bình"
    return "Yếu"


def student_summary(mssv):
    s = STUDENTS[mssv]
    avg = average(s["scores"])
    return {
        "mssv": mssv,
        "name": s["name"],
        "lop": s["lop"],
        "scores": dict(s["scores"]),
        "average": avg,
        "rank": rank(avg),
    }


def layout(title, body):
    menu = (
        f'<a href="{url_for("index")}">Trang chủ</a> · '
        f'<a href="{url_for("student_list")}">Sinh viên</a> · '
        f'<a href="{url_for("search")}">Tìm kiếm</a>'
    )
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>{escape(title)} - Sổ điểm</title>
</head>
<body>
<nav>{menu}</nav>
<hr>
{body}
</body>
</html>"""


@app.route("/")
def index():
    lops = {s["lop"] for s in STUDENTS.values()}
    body = (
        "<h1>Sổ điểm lớp học</h1>"
        f"<p>Tổng số sinh viên: {len(STUDENTS)}</p>"
        f"<p>Số lớp: {len(lops)}</p>"
        f'<p><a href="{url_for("student_list")}">Danh sách sinh viên</a> · '
        f'<a href="{url_for("api_students")}">API JSON</a></p>'
    )
    return layout("Trang chủ", body)


@app.route("/students")
def student_list():
    lop = request.args.get("lop", "").strip()

    # Thanh lọc: lấy các lớp từ dữ liệu, không viết cứng
    classes = sorted({s["lop"] for s in STUDENTS.values()})
    bar = f'<a href="{url_for("student_list")}">Tất cả</a>'
    for c in classes:
        bar += f' | <a href="{url_for("student_list", lop=c)}">{escape(c)}</a>'

    # Các dòng của bảng
    rows = ""
    for mssv in STUDENTS:
        info = student_summary(mssv)
        if lop and info["lop"].lower() != lop.lower():
            continue
        avg = "—" if info["average"] is None else info["average"]
        rows += (
            "<tr>"
            f'<td><a href="{url_for("student_detail", mssv=mssv)}">{escape(mssv)}</a></td>'
            f"<td>{escape(info['name'])}</td>"
            f"<td>{escape(info['lop'])}</td>"
            f"<td>{escape(avg)}</td>"
            f"<td>{escape(info['rank'])}</td>"
            "</tr>"
        )

    if rows:
        table = (
            '<table border="1" cellpadding="4">'
            "<tr><th>MSSV</th><th>Họ tên</th><th>Lớp</th>"
            "<th>Điểm TB</th><th>Xếp loại</th></tr>"
            f"{rows}</table>"
        )
    else:
        table = "<p>Không có sinh viên phù hợp.</p>"

    body = f"<h1>Danh sách sinh viên</h1><p>Lọc theo lớp: {bar}</p>{table}"
    return layout("Sinh viên", body)


# ---- Route tạm, sẽ làm thật ở các câu sau ----
@app.route("/students/<mssv>")
def student_detail(mssv):
    return layout("Chi tiết", "<p>Đang làm</p>")


@app.route("/search")
def search():
    return layout("Tìm kiếm", "<p>Đang làm</p>")


@app.route("/api/students")
def api_students():
    return "Đang làm"