import os
import sqlite3
import pandas as pd

from database import init_db

from agents.search_agent import (
    search_openalex,
    KEYWORDS
)

from agents.extraction_agent import (
    extract_research_data
)

DB_NAME = "research.db"

# Create fresh database every run

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

init_db()

conn = sqlite3.connect(DB_NAME)

for keyword in KEYWORDS:

    print(f"Searching: {keyword}")

    papers = search_openalex(keyword)

    print(f"Found {len(papers)} papers")

    for paper in papers:

        try:

            extracted = extract_research_data(
                paper["title"],
                paper["abstract"]
            )

            conn.execute("""
            INSERT INTO papers
            (
                title,
                authors,
                year,
                doi,
                journal,
                abstract,
                relevance_score,
                citation_count,
                access_type,
                pdf_available,
                pdf_link,
                repository_link,
                publisher_link,
                theory_primary,
                method,
                industry,
                country,
                keyword,
                source
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?
            )
            """,
            (
                paper["title"],
                paper["authors"],
                paper["year"],
                paper["doi"],
                paper["journal"],
                paper["abstract"],
                paper["relevance_score"],
                paper["citation_count"],
                paper["access_type"],
                paper["pdf_available"],
                paper["pdf_link"],
                paper["repository_link"],
                paper["publisher_link"],
                extracted["theory_primary"],
                extracted["method"],
                extracted["industry"],
                extracted["country"],
                paper["keyword"],
                paper["source"]
            ))

        except Exception as e:

            print(f"ERROR: {e}")

conn.commit()

df = pd.read_sql_query(
    "SELECT * FROM papers",
    conn
)

print(f"Total records: {len(df)}")

access_order = {
    "Open Access": 0,
    "Premium": 1
}

if "access_type" in df.columns:

    df["sort_order"] = df[
        "access_type"
    ].map(access_order)

    df = df.sort_values(
        by=[
            "sort_order",
            "relevance_score",
            "citation_count"
        ],
        ascending=[
            True,
            False,
            False
        ]
    )

    df = df.drop(
        columns=["sort_order"]
    )

df.to_excel(
    "work_disengagement_papers.xlsx",
    index=False
)

conn.close()

print(
    "Excel file created successfully."
)
