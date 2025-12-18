import json
import re
from collections import defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/documents.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

with open("data/assessments.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

TEST_TYPE_MAP = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

embeddings = np.load("data/embeddings.npy")

def normalize_test_type(raw_test_type):
    if not raw_test_type:
        return []
    if isinstance(raw_test_type, list):
        codes = raw_test_type
    elif isinstance(raw_test_type, str):
        codes = [x.strip() for x in raw_test_type.split(",")]
    else:
        return []
    return [TEST_TYPE_MAP.get(code, code) for code in codes]

# funct. to convert the duration(assessment_length) of string type into int type.
def normalize_duration(raw_length):
    
    if not raw_length:
        return None

    match = re.search(r"(\d+)", raw_length)
    if match:
        return int(match.group(1))
    return None


def balance(candidates, top_k):
    
    buckets = defaultdict(list)

    for item in candidates:
        types = item["test_type"]
        if not types:
            buckets["Other"].append(item)
        else:
            for t in types:
                buckets[t].append(item)

    balanced = []
    used_urls = set()

    while len(balanced) < top_k:
        added_in_round = False

        for test_type, items in buckets.items():
            for item in items:
                if item["assessment_url"] not in used_urls:
                    balanced.append(item)
                    used_urls.add(item["assessment_url"])
                    added_in_round = True
                    break

            if len(balanced) >= top_k:
                break

        if not added_in_round:
            break

    return balanced[:top_k]



def recommend_assessments(query, top_k=10):
    query_embedding = model.encode([query])

    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_index = np.argsort(scores)[::-1][:top_k*4]

    results = []
    for i in top_index:
        a = assessments[i]
        results.append({
            "assessment_name": a["name"],
            "assessment_url": a["url"],
            "description" : a["description"],
            "job_level" : a["job_levels"],
            #"languages" : a["languages"],
            "assessment_length" : normalize_duration(a.get("assessment_length")),
            "test_type" : normalize_test_type(a.get("test_type")),
             "score": float(scores[i])
        })


    #print(results[0])
    return balance(results, top_k)
