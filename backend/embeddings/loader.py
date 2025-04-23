import json
from pathlib import Path

QUIZ_PATH = Path(__file__).parent / "quizzes.json"

def load_quiz(skill: str, module_title: str):
    try:
        with open(QUIZ_PATH, "r", encoding="utf-8") as f:
            quizzes = json.load(f)
        for q in quizzes:
            if q["skill"].lower() == skill.lower() and q["module_title"].lower() == module_title.lower():
                return q["quiz"]
    except Exception:
        pass
    return None
