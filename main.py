import sqlite3
import pandas as pd

from database import init_db
from agents.search_agent import search_openalex, KEYWORDS

DB_NAME = "research.db"

init_db()

conn = sqlite3.connect(DB_NAME)

for keyword in KEYWORDS:

    print(f"Searching: {keyword}")

    papers = search_openalex(keyword)

    for paper in papers:

        try:

            conn.execute("""
            INSERT INTO papers
            (
                title,
                authors,
                year,
                doi,
                journal,
                keyword,
                source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                paper["title"],
                paper["authors"],
                paper["year"],
                paper["doi"],
                paper["journal"],
                paper["keyword"],
                paper["source"]
            ))

        except Exception:
            pass

conn.commit()

df = pd.read_sql_query(
    "SELECT * FROM papers",
    conn
)

df.to_excel(
    "work_disengagement_papers.xlsx",
    index=False
)

conn.close()

print("Finished.")
