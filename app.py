from flask import Flask, render_template, request, redirect, flash
import os
import ollama

from database import init_db
from models import save_exam, get_all_exams
from ollama_utils import extract_exam_data
from study_planner import generate_plan

app = Flask(__name__)
app.secret_key = "studyplanner"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        flash("No image uploaded")
        return redirect("/")

    file = request.files["image"]

    if file.filename == "":
        flash("Please select an image")
        return redirect("/")

    path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(path)

    print(f"Saved Image: {path}")

    try:
        exams = extract_exam_data(path)

        print("Extracted Exams:")
        print(exams)

        for exam in exams:

            if (
                "subject" in exam and
                "exam_date" in exam
            ):
                save_exam(
                    exam["subject"],
                    exam["exam_date"]
                )

    except Exception as e:
        print("Extraction Error:", e)
        flash(f"Error: {e}")
        return redirect("/")

    return redirect("/planner")


@app.route("/planner")
def planner():

    exams = get_all_exams()

    data = []

    for exam in exams:
        data.append({
            "subject": exam["subject"],
            "exam_date": exam["exam_date"]
        })

    plan = ""

    if len(data) > 0:
        plan = generate_plan(data)

    return render_template(
        "planner.html",
        exams=exams,
        plan=plan
    )


@app.route("/chat", methods=["GET", "POST"])
def chat():

    answer = ""

    if request.method == "POST":

        question = request.form["message"]

        exams = get_all_exams()

        memory = ""

        for e in exams:
            memory += (
                f"Subject: {e['subject']}, "
                f"Exam Date: {e['exam_date']}\n"
            )

        prompt = f"""
You are a Study Planner Assistant.

Saved Exams:

{memory}

Answer only using the stored exams.

Question:
{question}
"""

        try:

            response = ollama.chat(
                model="llama3.2:latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"]

        except Exception as e:
            answer = f"Error: {str(e)}"

    return render_template(
        "chat.html",
        answer=answer
    )


if __name__ == "__main__":
    app.run(debug=True)