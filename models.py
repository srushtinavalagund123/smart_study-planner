from database import get_connection


def save_exam(subject, exam_date):
    conn = get_connection()

    conn.execute(
        "INSERT INTO exams(subject,exam_date) VALUES(?,?)",
        (subject, exam_date)
    )

    conn.commit()
    conn.close()


def get_all_exams():
    conn = get_connection()

    exams = conn.execute(
        "SELECT * FROM exams ORDER BY exam_date"
    ).fetchall()

    conn.close()
    return exams