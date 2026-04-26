import os
import requests
from flask import Flask, render_template, request
from utils.extractor import extract_text_from_pdf

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔗 Hugging Face API
HF_API_URL = "https://huggingface.co/spaces/Roshni123456/Resumeml/run/predict"

# Sample job descriptions
JOB_DESCRIPTIONS = {
    "Data Scientist": "Machine learning, Python, statistics, data analysis",
    "Web Developer": "HTML, CSS, JavaScript, React, backend development",
    "AI Engineer": "Deep learning, NLP, PyTorch, TensorFlow"
}

def get_match_score(resume_text, job_desc):
    payload = {"data": [resume_text, job_desc]}
    response = requests.post(HF_API_URL, json=payload)

    if response.status_code != 200:
        return "Error from ML API"

    result = response.json()
    return result["data"][0]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["resume"]
    role = request.form["role"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    resume_text = extract_text_from_pdf(filepath)
    job_desc = JOB_DESCRIPTIONS.get(role, "")

    score = get_match_score(resume_text, job_desc)

    return render_template("result.html", score=score, role=role)

if __name__ == "__main__":
    app.run(debug=True)