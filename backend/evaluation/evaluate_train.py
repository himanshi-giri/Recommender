#from urllib.parse import urlparse
import re
import pandas as pd
from services.recommender import recommend_assessments

# def normalize_url(url):
    
#     if not url:
#         return None

#     url = url.strip()

#     if url.startswith("http"):
#         return urlparse(url).path.rstrip("/")

#     return url.rstrip("/")

def normalize_url(url):
    if not isinstance(url, str):
        return None

    match = re.search(r"/product-catalog/view/[^/]+/", url)
    if match:
        return match.group(0)
    return None


K = 10
print("Starting evaluation..")

def recall_at_k(predicted, relevant, k=10):
    predicted_k = predicted[:k]
    hit_count = len(set(predicted_k) & set(relevant))
    return hit_count / len(relevant) if relevant else 0

train_df = pd.read_excel("data/Gen_AI_Dataset.xlsx", sheet_name="Train-Set")

recalls = []

for idx, row in train_df.iterrows():
    query = row["Query"]
    print("Evaluating query:", query)
    
    if pd.isna(row["Assessment_url"]):
        continue

    relevant = [
        normalize_url(x)
        for x in row["Assessment_url"].split(",")
    ]

    predictions = recommend_assessments(query, top_k=K)
    predicted_urls = [normalize_url(p["assessment_url"]) for p in predictions]

    r = recall_at_k(predicted_urls, relevant, K)
    recalls.append(r)

mean_recall = sum(recalls) / len(recalls)

print(f"Mean Recall@{K}: {mean_recall:.4f}")
