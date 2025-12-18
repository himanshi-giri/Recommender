# Data preparation.
import json
import re

with open("data/assessments.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

documents = []

for a in assessments:
    name = a.get("name") or ""
    desc = a.get("description") or ""
    job = a.get("job_levels") or ""
    lang = a.get("languages") or ""
    length = a.get("assessment_length") or ""
    test_type = a.get("test_type") or ""

    text = f"""
     This assessment helps evaluate candidates for the role of {name}.
    It measures skills and abilities related to {desc}.
    Suitable for job levels: {job}.
    Used to assess candidates during hiring, screening, and talent evaluation.
    Assessment focuses on {test_type} competencies.
    

    """

    documents.append({
       # "text": text.strip(),
       "text": re.sub(r"\s+", " ", text.strip()),
        "url": a.get("url"),
        "name": a.get("name")
    })

with open("data/documents.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2, ensure_ascii=False)

print("Documents prepared:", len(documents))