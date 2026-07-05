import pandas as pd
import json
import os

RAW_DIR = "onet_raw"
OUTPUT_FILE = "career_kb.jsonl"

VALID_INTEREST_TYPES = {
    "Realistic", "Investigative", "Artistic",
    "Social", "Enterprising", "Conventional"
}

def load_onet_data():
    occupations = pd.read_csv(
        os.path.join(RAW_DIR, "Occupation Data.txt"), sep="\t"
    )
    skills = pd.read_csv(
        os.path.join(RAW_DIR, "Essential Skills.txt"), sep="\t"
    )
    interests = pd.read_csv(
        os.path.join(RAW_DIR, "Career Interest Types.txt"), sep="\t"
    )
    return occupations, skills, interests

def build_documents(occupations, skills, interests):
    docs = []
    for _, row in occupations.iterrows():
        code = row["O*NET-SOC Code"]
        title = row["Title"]
        description = row["Description"]

        related_skills = skills[skills["O*NET-SOC Code"] == code]
        # Dedupe skill names (they can repeat across scale types) and keep highest value per skill
        deduped_skills = (
            related_skills.groupby("Element Name")["Data Value"]
            .max()
            .sort_values(ascending=False)
            .head(8)
        )
        top_skills = deduped_skills.index.tolist()

        related_interests = interests[
            (interests["O*NET-SOC Code"] == code)
            & (interests["Element Name"].isin(VALID_INTEREST_TYPES))
        ]
        top_interests = (
            related_interests.sort_values("Data Value", ascending=False)
            .head(3)["Element Name"]
            .tolist()
        )

        doc_text = (
            f"Career: {title}\n"
            f"Description: {description}\n"
            f"Key Skills Required: {', '.join(top_skills)}\n"
            f"Personality/Interest Traits: {', '.join(top_interests)}. "
            f"This career suits people who are {', '.join(top_interests).lower()}-oriented."
        )

        docs.append({
            "id": code,
            "title": title,
            "text": doc_text
        })
    return docs

if __name__ == "__main__":
    occupations, skills, interests = load_onet_data()
    docs = build_documents(occupations, skills, interests)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc) + "\n")

    print(f"Created {len(docs)} career documents in {OUTPUT_FILE}")