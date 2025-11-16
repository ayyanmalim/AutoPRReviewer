from fastapi import FastAPI
from pydantic import BaseModel
import pymysql

app = FastAPI()

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="autopr_db",
        cursorclass=pymysql.cursors.DictCursor
    )

class PullRequest(BaseModel):
    title: str
    description: str
    diff_text: str


def analyze_diff(diff_text: str):
    comments = []
    lines = diff_text.split("\n")

    for i, line in enumerate(lines, start=1):

        if "password" in line and "==" in line:
            comments.append({
                "filename": "unknown_file",
                "line_number": i,
                "issue": "Insecure password comparison '==' detected.",
                "suggestion": "Use a secure hash comparison method instead."
            })

        if "API_KEY" in line or "SECRET" in line:
            comments.append({
                "filename": "unknown_file",
                "line_number": i,
                "issue": "Hardcoded secret/API key found.",
                "suggestion": "Move secrets into environment variables."
            })

        if "print(" in line:
            comments.append({
                "filename": "unknown_file",
                "line_number": i,
                "issue": "Debug print statement found.",
                "suggestion": "Remove debug logs before committing."
            })

    return comments

@app.post("/pull_request")
def create_pull_request(pr: PullRequest):
    comments = analyze_diff(pr.diff_text)

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO pull_requests (title, description, diff_text) VALUES (%s, %s, %s)",
        (pr.title, pr.description, pr.diff_text)
    )
    pr_id = cursor.lastrowid

    for c in comments:
        cursor.execute(
            "INSERT INTO review_comments (pr_id, filename, line_number, issue, suggestion) VALUES (%s, %s, %s, %s, %s)",
            (pr_id, c["filename"], c["line_number"], c["issue"], c["suggestion"])
        )

    db.commit()
    cursor.close()
    db.close()

    return {
        "pr_id": pr_id,
        "message": "PR stored successfully. Review comments generated.",
        "review_comments": comments
    }

@app.get("/pull_requests")
def list_pull_requests():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pull_requests")
    data = cursor.fetchall()
    db.close()
    return data

@app.get("/review_comments/{pr_id}")
def get_comments(pr_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM review_comments WHERE pr_id=%s", (pr_id,))
    data = cursor.fetchall()
    db.close()
    return data
