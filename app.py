from flask import Flask, render_template, request, redirect, url_for
import os, json

from utils.parser import extract_text
from utils.extractor import extract_skills
from utils.ats_score import ats_score
from utils.suggestions import generate_suggestions
from models.similarity import get_similarity

import os
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs("uploads", exist_ok=True)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load data
with open("data/job_roles.json") as f:
    JOB_ROLES = json.load(f)

with open("data/interview_data.json") as f:
    INTERVIEW_DB = json.load(f)

@app.route("/")
def home():
    return render_template("index.html", roles=JOB_ROLES.keys())

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["resume"]
    role = request.form["role"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    resume_text = extract_text(filepath)
    skills = extract_skills(resume_text)

    job_desc = JOB_ROLES[role]

    similarity = get_similarity(resume_text, job_desc)
    ats = ats_score(skills, job_desc)

    job_skills = job_desc.lower().split(", ")
    missing = [s for s in job_skills if s not in skills]

    suggestions = generate_suggestions(missing)

    return render_template("result.html",
                           role=role,
                           skills=skills,
                           missing=missing,
                           suggestions=suggestions,
                           similarity=round(similarity*100,2),
                           ats=round(ats,2))

# INTERVIEW BOT
@app.route("/interview/<role>")
def interview(role):
    questions = INTERVIEW_DB.get(role, [])
    return render_template("interview.html", role=role, questions=questions)

@app.route("/submit_interview", methods=["POST"])
def submit_interview():
    role = request.form["role"]
    new_question = request.form["new_question"]

    if new_question:
        INTERVIEW_DB[role].append(new_question)
        with open("data/interview_data.json","w") as f:
            json.dump(INTERVIEW_DB, f, indent=4)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
