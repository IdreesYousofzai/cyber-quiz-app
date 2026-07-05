# 🛡️ Cyber Security Quiz App

A Flask web app that tests your knowledge of cyber security with 15 multiple-choice
questions covering phishing, malware, encryption, network security, and UK law
(Computer Misuse Act 1990). Built as part of my cyber security / software
development portfolio.

**🔗 Live demo:** https://idrees200.pythonanywhere.com/

<img width="689" height="401" alt="image" src="https://github.com/user-attachments/assets/1477b084-1144-4d0a-bc71-e5bc56b0d81a" />

---

## Features

- 15 cyber security questions stored in `questions.json`, each with 4 options,
  the correct answer, and a brief explanation
- Session-based tracking of the user's answers and score across pages (no database needed)
- Live progress bar showing how far through the quiz the user is
- Results page with final score, a letter grade, and a full question-by-question
  review with colour-coded correct/incorrect feedback
- Clean, responsive, professional UI styled with custom CSS (no frameworks)
- "Try Again" button that resets the session and restarts the quiz

---

## Project structure

```
cyber-quiz-app/
├── app.py               # Flask app: routes, session logic, scoring
├── questions.json        # 15 quiz questions (options, answer, explanation)
├── requirements.txt      # Python dependencies
├── README.md
├── templates/
│   ├── base.html          # Shared layout (header/footer)
│   ├── home.html          # Landing page
│   ├── question.html      # Quiz question page + progress bar
│   └── results.html       # Score, grade, and full breakdown
└── static/
    └── style.css           # All styling
```

## Routes

| Route                     | Method   | Purpose                                             |
|---------------------------|----------|------------------------------------------------------|
| `/`                       | GET      | Home page. Clears session to start a fresh attempt.  |
| `/question/<int:num>`     | GET      | Displays question `num` (1–15) with progress bar.    |
| `/question/<int:num>`     | POST     | Saves the selected answer, moves to next question.   |
| `/results`                | GET      | Calculates score/grade and shows full review.        |
| `/reset`                  | GET      | Clears the session ("Try Again").                    |

Answers are stored in the Flask **session** (a signed cookie), keyed by question
number, so the score is only calculated once at the end from the full set of
answers — this avoids double-counting if a user navigates back and forth.

---

## Running locally

1. Clone the repo and move into it:
   ```bash
   git clone https://github.com/IdreesYousofzai/cyber-quiz-app.git
   cd cyber-quiz-app
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000`

---

## Deploying for free on PythonAnywhere

1. **Create an account** at [pythonanywhere.com](https://www.pythonanywhere.com)
   (the free "Beginner" tier is enough for this project).

2. **Upload your code.** Easiest way — open a **Bash console** on PythonAnywhere
   and clone your GitHub repo:
   ```bash
   git clone https://github.com/IdreesYousofzai/cyber-quiz-app.git
   ```

3. **Create a virtual environment** in the same Bash console:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 cyberquiz-venv
   pip install -r cyber-quiz-app/requirements.txt
   ```

4. **Create a new web app:**
   - Go to the **Web** tab → **Add a new web app**
   - Choose **Manual configuration** (not the Flask wizard) → select your Python version

5. **Point it at your virtualenv:**
   - In the **Virtualenv** section of the Web tab, enter the path
     (e.g. `/home/<your-username>/.virtualenvs/cyberquiz-venv`)

6. **Edit the WSGI config file** (linked near the top of the Web tab). Replace its
   contents with:
   ```python
   import sys
   path = '/home/<your-username>/cyber-quiz-app'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```

7. **Set your secret key as an environment variable** (recommended): in the
   **Web** tab, under "Environment variables", add `SECRET_KEY` with a long
   random string. If skipped, the app falls back to a default dev key — fine
   for a demo, not for production.

8. Make sure the **Static files** mapping points `/static/` to
   `/home/<your-username>/cyber-quiz-app/static/`.

9. Click the big green **Reload** button at the top of the Web tab.

10. Visit `https://<your-username>.pythonanywhere.com` — your quiz is live!

---

## Possible future improvements

- Add a timer per question
- Store high scores using a small database (e.g. SQLite)
- Add difficulty levels (Beginner / Intermediate / Advanced question sets)
- Add a shareable results image/summary

---

## Author

Idrees Yousofzai — T-Level Digital Software Development, Blackburn College
