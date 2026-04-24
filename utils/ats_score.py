def ats_score(resume_skills, job_desc):
    job_desc = job_desc.lower()
    job_skills = job_desc.split(", ")

    matched = len([s for s in resume_skills if s in job_desc])
    total = len(job_skills)

    return (matched / total) * 100 if total > 0 else 0