"""
Cyber Security Quiz Web App
----------------------------
A Flask app that quizzes users on 15 cyber security questions,
tracks their answers/score using sessions, and shows a full
results breakdown at the end.
"""

from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
# Secret key is required for Flask sessions to work (signs the session cookie).
# In production, set this via an environment variable instead of hardcoding it.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-this-in-production")

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "questions.json")


def load_questions():
    """Load the quiz questions from the JSON file."""
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


QUESTIONS = load_questions()
TOTAL_QUESTIONS = len(QUESTIONS)


@app.route("/")
def home():
    """Home page. Starting a new quiz clears any previous session data."""
    session.clear()
    return render_template("home.html", total=TOTAL_QUESTIONS)


@app.route("/question/<int:num>", methods=["GET", "POST"])
def question(num):
    """
    Show question `num` (1-indexed) and handle the submitted answer.
    On POST: store the chosen answer in the session, then move to the
    next question or to the results page if this was the last question.
    """
    # Guard against invalid or out-of-range question numbers.
    if num < 1 or num > TOTAL_QUESTIONS:
        return redirect(url_for("home"))

    # Make sure the user has started a quiz (answers dict exists in session).
    if "answers" not in session:
        session["answers"] = {}

    if request.method == "POST":
        selected = request.form.get("option")
        if selected is not None:
            # Store answers keyed by question number (as string, since
            # session data is JSON-serialisable and dict keys become strings).
            answers = session["answers"]
            answers[str(num)] = int(selected)
            session["answers"] = answers
            session.modified = True

        if num < TOTAL_QUESTIONS:
            return redirect(url_for("question", num=num + 1))
        else:
            return redirect(url_for("results"))

    question_data = QUESTIONS[num - 1]
    progress_percent = round((num - 1) / TOTAL_QUESTIONS * 100)

    return render_template(
        "question.html",
        question=question_data,
        num=num,
        total=TOTAL_QUESTIONS,
        progress_percent=progress_percent,
    )


@app.route("/results")
def results():
    """Calculate the final score and show a full breakdown of every question."""
    answers = session.get("answers", {})

    breakdown = []
    score = 0

    for index, q in enumerate(QUESTIONS):
        q_num = index + 1
        user_answer_index = answers.get(str(q_num))
        is_correct = user_answer_index == q["answer"]

        if is_correct:
            score += 1

        breakdown.append({
            "num": q_num,
            "question": q["question"],
            "options": q["options"],
            "correct_index": q["answer"],
            "correct_text": q["options"][q["answer"]],
            "user_index": user_answer_index,
            "user_text": q["options"][user_answer_index] if user_answer_index is not None else "No answer given",
            "is_correct": is_correct,
            "explanation": q["explanation"],
        })

    percentage = round((score / TOTAL_QUESTIONS) * 100)

    if percentage >= 90:
        grade = "A*"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    return render_template(
        "results.html",
        score=score,
        total=TOTAL_QUESTIONS,
        percentage=percentage,
        grade=grade,
        breakdown=breakdown,
    )


@app.route("/reset")
def reset():
    """Clear the session and start again."""
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
