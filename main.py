import sqlite3
import pandas as pd

from database import init_db

from agents.search_agent import (
    search_openalex,
    KEYWORDS
)

DB_NAME = "research.db"

init_db()

conn = sqlite3.connect(
    DB_NAME
)

for keyword in KEYWORDS:

    print(
        f"Searching: {keyword}"
    )

    papers = search_openalex(
        keyword
    )

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
                abstract,
                relevance_score,
                citation_count,
                access_type,
                pdf_available,
                pdf_link,
                repository_link,
                publisher_link,
                keyword,
                source
            )
            VALUES
            (
                ?,?,?,?,?,?,
                ?,?,?,?,?,?,
                ?,?,?,?
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
                paper["keyword"],
                paper["source"]
            ))

        except Exception:

            pass

conn.commit()

df = pd.read_sql_query(
    """
    SELECT *
    FROM papers
    """,
    conn
)

if (
    "access_type" in df.columns
    and
    "relevance_score"
    in df.columns
):

    access_order = {

        "Open Access": 0,

        "Premium": 1
    }

    df[
        "sort_order"
    ] = df[
        "access_type"
    ].map(
        access_order
    )

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
        columns=[
            "sort_order"
        ]
    )

df.to_excel(
    "work_disengagement_papers.xlsx",
    index=False
)

conn.close()

print("Finished.")
