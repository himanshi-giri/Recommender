from fastapi import APIRouter
from services.recommender import recommend_assessments

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok."}

@router.post("/recommend")
def recommend(payload: dict):
    query = payload.get("query")

    if not query:
        return {"error": "Query is missing."}
    results = recommend_assessments(query, top_k = 10)

    return{
        "query": query,
        "recommendations": [
            {
                "assessment_name": r["assessment_name"],
                "assessment_url": r["assessment_url"],
                "description" : r["description"],
                "assessment_length" : r["assessment_length"],
                "test_type" : r["test_type"],
            }
            for r in results
        ]
    }