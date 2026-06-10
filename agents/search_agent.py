import requests

BASE_URL = "https://api.openalex.org/works"

KEYWORDS = [
    "work disengagement",
    "employee disengagement",
    "job disengagement",
    "work withdrawal",
    "psychological withdrawal",
    "quiet quitting",
    "employee withdrawal",
    "burnout disengagement"
]


def search_openalex(keyword, per_page=50):

    params = {
        "search": keyword,
        "per-page": per_page
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"Error searching {keyword}")
        return []

    data = response.json()

    papers = []

    for item in data.get("results", []):

        title = item.get("title", "")

        year = item.get("publication_year")

        doi = item.get("doi")

        journal = ""

        if item.get("primary_location"):

            source = item["primary_location"].get("source")

            if source:
                journal = source.get(
                    "display_name",
                    ""
                )

        authors = []

        for a in item.get("authorships", []):

            author = a.get("author", {})

            authors.append(
                author.get(
                    "display_name",
                    ""
                )
            )

        open_access = item.get(
            "open_access",
            {}
        )

        pdf_link = open_access.get(
            "oa_url"
        )

        access_type = (
            "Open Access"
            if open_access.get(
                "is_oa"
            )
            else "Premium"
        )

        pdf_available = (
            "Yes"
            if pdf_link
            else "No"
        )

        landing_page = ""

        if item.get("primary_location"):

            landing_page = item[
                "primary_location"
            ].get(
                "landing_page_url",
                ""
            )

        papers.append({

            "title": title,

            "authors": ", ".join(
                authors
            ),

            "year": year,

            "doi": doi,

            "journal": journal,

            "abstract": str(
                item.get(
                    "abstract_inverted_index",
                    {}
                )
            ),

            "citation_count": item.get(
                "cited_by_count",
                0
            ),

            "access_type": access_type,

            "pdf_available": pdf_available,

            "pdf_link": pdf_link,

            "repository_link": landing_page,

            "publisher_link": landing_page,

            "keyword": keyword,

            "source": "OpenAlex"
        })

    return papers
