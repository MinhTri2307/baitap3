import math

from flask import (Flask, abort, jsonify, make_response, redirect, request,
                   url_for)
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

    classes = sorted({s["lop"] for s in STUDENTS.values()})
    bar = f'<a href="{url_for("student_list")}">Tất cả</a>'
    for c in classes:
        bar += f' | <a href="{url_for("student_list", lop=c)}">{escape(c)}</a>'

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


@app.route("/students/<mssv>")
def student_detail(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    info = student_summary(mssv)
    avg = "—" if info["average"] is None else info["average"]

    if info["scores"]:
        rows = ""
        for course, score in info["scores"].items():
            rows += f"<tr><td>{escape(course)}</td><td>{escape(score)}</td></tr>"
        score_table = (
            '<table border="1" cellpadding="4">'
            "<tr><th>Học phần</th><th>Điểm</th></tr>"
            f"{rows}</table>"
        )
    else:
        score_table = "<p>Chưa có điểm học phần nào.</p>"

    short = url_for("student_short", mssv=mssv)
    body = (
        f"<h1>{escape(info['name'])}</h1>"
        f"<p>MSSV: {escape(mssv)}</p>"
        f'<p>Lớp: <a href="{url_for("student_list", lop=info["lop"])}">'
        f'{escape(info["lop"])}</a></p>'
        f"<p>Điểm TB: {escape(avg)}</p>"
        f"<p>Xếp loại: {escape(info['rank'])}</p>"
        f"<h2>Bảng điểm</h2>{score_table}"
        f'<p><a href="{url_for("student_export", mssv=mssv)}">'
        "Tải bảng điểm (CSV)</a></p>"
        f"<p>Link rút gọn: <code>{escape(short)}</code></p>"
    )
    return layout(info["name"], body)


@app.route("/sv/<mssv>")
def student_short(mssv):
    return redirect(url_for("student_detail", mssv=mssv), code=301)


@app.route("/students/<mssv>/export")
def student_export(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    lines = ["hoc_phan,diem"]
    for course, score in STUDENTS[mssv]["scores"].items():
        lines.append(f"{course},{score}")
    resp = make_response("\n".join(lines) + "\n")
    resp.headers["Content-Type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    return resp


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    form = (
        f'<form method="get" action="{url_for("search")}">'
        f'<input type="text" name="q" value="{escape(q)}">'
        '<button type="submit">Tìm</button>'
        "</form>"
    )

    result = ""
    if q:
        key = q.lower()
        found = [
            m for m, s in STUDENTS.items()
            if key in s["name"].lower() or key in m.lower()
        ]
        items = ""
        for m in found:
            items += (
                f'<li><a href="{url_for("student_detail", mssv=m)}">'
                f'{escape(m)} - {escape(STUDENTS[m]["name"])}</a></li>'
            )
        result = (
            f"<p>Tìm thấy {len(found)} kết quả cho “{escape(q)}”</p>"
            f"<ul>{items}</ul>"
        )

    body = f"<h1>Tìm kiếm sinh viên</h1>{form}{result}"
    return layout("Tìm kiếm", body)


def parse_float(raw):
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value):
        return None
    return value


@app.route("/api/students")
def api_students():
    lop = request.args.get("lop")
    raw_min = request.args.get("min_avg")

    min_avg = None
    if raw_min is not None:
        min_avg = parse_float(raw_min)
        if min_avg is None:
            abort(400, description=f"min_avg phải là số, nhận được: {raw_min!r}.")

    result = []
    for mssv in STUDENTS:
        info = student_summary(mssv)
        if lop is not None and info["lop"].lower() != lop.lower():
            continue
        if min_avg is not None:
            if info["average"] is None or info["average"] < min_avg:
                continue
        result.append(info)
    return jsonify(result)


@app.route("/api/students/<mssv>")
def api_student(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    return jsonify(student_summary(mssv))


@app.route("/api/students/<mssv>/scores/<course>",
           methods=["GET", "PUT", "DELETE"])
def api_score(mssv, course):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    course = course.upper()
    scores = STUDENTS[mssv]["scores"]

    if request.method == "PUT":
        raw = request.args.get("score")
        if raw is None:
            abort(400, description="Thiếu tham số score.")
        score = parse_float(raw)
        if score is None:
            abort(400, description=f"score phải là số, nhận được: {raw!r}.")
        if not 0 <= score <= 10:
            abort(400, description="score phải nằm trong khoảng [0, 10].")

        existed = course in scores
        scores[course] = score
        resp = jsonify({
            "mssv": mssv,
            "course": course,
            "score": score,
            "average": average(scores),
        })
        if not existed:
            resp.status_code = 201
            resp.headers["Location"] = url_for("api_score", mssv=mssv,
                                               course=course)
        return resp

    if course not in scores:
        abort(404, description=f"{mssv} chưa có điểm học phần {course}.")

    if request.method == "DELETE":
        del scores[course]
        return "", 204

    return jsonify({"mssv": mssv, "course": course, "score": scores[course]})