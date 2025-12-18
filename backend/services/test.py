from recommender import recommend_assessments
if __name__ == "__main__":
    query = "Hirirng a software developer with good teamwork skills"
    results = recommend_assessments(query)

    for r in results:
        print(r["assessment_name"], "->", r["assessment_url"])