import re

SKILLS_DB = [
    "python","java","machine learning","deep learning",
    "nlp","sql","flask","django","react","docker",
    "tensorflow","pytorch","statistics"
]

def extract_skills(text):
    text = text.lower()
    skills = set()

    for skill in SKILLS_DB:
        if re.search(r"\b" + skill + r"\b", text):
            skills.add(skill)

    return list(skills)