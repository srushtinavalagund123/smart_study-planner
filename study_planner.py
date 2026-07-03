from datetime import datetime
import ollama


def calculate_days(exam_date):

    today = datetime.now().date()

    exam = datetime.strptime(
        exam_date,
        "%Y-%m-%d"
    ).date()

    return (exam - today).days


def generate_plan(exams):

    context = ""

    for exam in exams:

        days = calculate_days(
            exam["exam_date"]
        )

        context += f"""
Subject: {exam['subject']}
Exam Date: {exam['exam_date']}
Days Left: {days}
"""

    prompt = f"""
You are a Study Planning Agent.

Generate a daily study schedule.

{context}

Rules:
1. More focus on nearest exams.
2. Give hours per day.
3. Output clean table.
"""

    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]