🤖 Automated Pull Request Review Agent
Built with FastAPI + MySQL (Backend Engineering Assignment)

Hello! 👋
This project is my submission for the Lyzr AI Backend Engineering Intern Challenge.
The goal is to build a backend system that can review GitHub Pull Request code changes and generate useful review comments automatically.

This project does not use any paid APIs and works fully offline.
I created a simple rule-based code reviewer that analyzes PR diffs and identifies some common issues.

📌 What This Project Can Do

When a user submits a pull request through API, the system:

🔍 Reads the diff text (code changes)
🧠 Analyzes the code for risky patterns
📝 Generates review comments if issues are found
💾 Saves PR and comments into a MySQL database
📤 Allows API users to retrieve PRs and comments anytime

🧠 Current Review Rules Implemented

The agent can detect the following:

Issue Detected	Example Code	Suggested Fix
Insecure password comparison	password == input	Use secure hashing
Hardcoded API keys/secrets	API_KEY = 'ABC123'	Move to environment variables
Debug print statements	print("test")	Remove or use logging

If the diff text does not contain any of these patterns, no comments are added.

🛠 Tech Stack
Component	Technology
Backend Framework	FastAPI
Language	Python
Database	MySQL (Using PyMySQL)
API Docs	Swagger UI (/docs)
📡 API Endpoints
Method	Endpoint	Description
POST	/pull_request	Submit a PR and generate comments
GET	/pull_requests	List all stored PRs
GET	/review_comments/{pr_id}	Get review comments for a PR
🧪 How to Test (Example Inputs)
1️⃣ Example that generates comments
{
  "title": "Fix login issue",
  "description": "Insecure password comparison fixed",
  "diff_text": "if(password == input){ print('debug'); }"
}

2️⃣ Example that generates comments
{
  "title": "Removed API key",
  "description": "Security improvement",
  "diff_text": "const API_KEY = '12345SECRET';"
}

3️⃣ Example that returns no comments
{
  "title": "UI update",
  "description": "Updated button color",
  "diff_text": "button.color = 'blue';"
}

🛢 Database Setup (SQL)
CREATE DATABASE autopr_db;
USE autopr_db;

CREATE TABLE pull_requests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  diff_text LONGTEXT
);

CREATE TABLE review_comments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pr_id INT,
  filename VARCHAR(255),
  line_number INT,
  issue TEXT,
  suggestion TEXT,
  FOREIGN KEY (pr_id) REFERENCES pull_requests(id) ON DELETE CASCADE
);

▶ Run the Project
uvicorn main:app --reload


Open Swagger UI for testing:
👉 http://127.0.0.1:8000/docs

📽 Demonstration (Recording Guidance)

In the demo, I will show:

1️⃣ Submitting a PR with insecure code → comments appear
2️⃣ Submitting a PR with no risky code → no comments
3️⃣ Viewing all PRs
4️⃣ Viewing review comments for a specific PR

This proves the system logic works correctly.

👨‍💻 About Me (Short Self Intro)

I am passionate about Backend Development and APIs.
I enjoy building real-world systems that solve problems.
This project helped me learn:

✔ FastAPI routing and request handling
✔ Working with MySQL from Python
✔ Designing clean API responses
✔ Simulating automated code review logic

🚀 Future Improvements

If I get the opportunity to continue working on this project, I would like to improve it by:

🔧 Adding real AI/LLM review analysis
🌿 Supporting multiple files in a PR
🎯 Providing severity levels (high/medium/low)
🛡 Detecting more security and performance issues

🙏 Thank You

Thank you for reviewing my backend project!
I am excited about the opportunity to learn, contribute, and grow as an engineer.
