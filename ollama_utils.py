import ollama
import json
import re


def extract_exam_data(image_path):

    response = ollama.chat(
        model="llava:latest",
        messages=[
            {
                "role": "user",
                "content": """
Extract exam subjects and exam dates.

Return ONLY valid JSON.

Example:

[
  {
    "subject":"DBMS",
    "exam_date":"2026-06-25"
  }
]

If no exams are found return:
[]
                """,
                "images": [image_path]
            }
        ]
    )

    text = response["message"]["content"]

    print("\n===== LLAVA OUTPUT =====")
    print(text)
    print("========================\n")

    match = re.search(r"\[.*\]", text, re.DOTALL)

    if not match:
        return []

    try:
        return json.loads(match.group())
    except Exception as e:
        print("JSON ERROR:", e)
        print("BAD JSON:", match.group())
        return []