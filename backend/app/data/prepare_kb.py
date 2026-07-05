import pandas as pd
import json
import os

RAW_DIR = "onet_raw"
OUTPUT_FILE = "career_kb.jsonl"

def load_onet_data():
    occupations = pd.read_csv(
        os.path.join(RAW_DIR, "Occupation Data.txt"), sep="\t"
    )
    skills = pd.read_csv(
    os.path.join(RAW_DIR, "Essential Skills.txt"), sep="\t"
    )
    return occupations, skills

def build_documents(occupations, skills):
    docs = []
    for _, row in occupations.iterrows():
        code = row["O*NET-SOC Code"]
        title = row["Title"]
        description = row["Description"]

        related_skills = skills[skills["O*NET-SOC Code"] == code]
        top_skills = (
            related_skills.sort_values("Data Value", ascending=False)
            .head(8)["Element Name"]
            .tolist()
        )

        doc_text = (
            f"Career: {title}\n"
            f"Description: {description}\n"
            f"Key Skills Required: {', '.join(top_skills)}"
        )

        docs.append({
            "id": code,
            "title": title,
            "text": doc_text
        })
    return docs

if __name__ == "__main__":
    occupations, skills = load_onet_data()
    docs = build_documents(occupations, skills)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc) + "\n")

    print(f"Created {len(docs)} career documents in {OUTPUT_FILE}")