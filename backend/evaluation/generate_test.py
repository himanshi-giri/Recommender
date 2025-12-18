import pandas as pd
from services.recommender import recommend_assessments

test_data = pd.read_excel("data/Gen_AI_Dataset.xlsx", sheet_name="Test-Set")

rows = []

for _, row in test_data.iterrows():
    query = row["Query"]

    predictions = recommend_assessments(query, top_k=10)

    for p in predictions:
        rows.append({
            "Query": query,
            "Assessment_url": p["assessment_url"]
        })

output = pd.DataFrame(rows)
output.to_csv("evaluation/submission_predictions.csv", index=False)

print("submission_predictions.csv generated successfully")
