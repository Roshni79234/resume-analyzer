import os
import requests
from flask import Flask, render_template, request
from utils.extractor import extract_text_from_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔗 Hugging Face API
HF_API_URL = "HF_API_URL = "https://roshni123456-resumeml.hf.space/run/predict""

# Job roles
JOB_DESCRIPTIONS = {
    "Data Scientist": "Machine learning, Python, statistics, data analysis",
    "Web Developer": "HTML, CSS, JavaScript, React, backend development",
    "AI Engineer": "Deep learning, NLP, PyTorch, TensorFlow"
}

# 🔥 API CALL FUNCTION
def get_match_score(resume_text, job_desc):
    payload = {"data": [resume_text, job_desc]}

    try:
        response = requests.post(HF_API_URL, json=payload)

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code != 200:
            return "API Error"

        result = response.json()
        return result["data"][0]

    except Exception as e:
        print("ERROR:", e)
        return "API Error"


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

    print("Resume length:", len(resume_text))

    score = get_match_score(resume_text, job_desc)

    return render_template("result.html", score=score, role=role)


# ✅ FIXED INTERVIEW ROUTE
@app.route("/interview")
def interview():
    return render_template("interview.html")


if __name__ == "__main__":
    app.run(debug=True)