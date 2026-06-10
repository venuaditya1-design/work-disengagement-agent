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


def reconstruct_abstract(inverted_index):

    if not inverted_index:
        return ""

    words = []

    for word, positions in inverted_index.items():

        for pos in positions:

            words.append(
                (pos, word)
            )

    words.sort()

    return " ".join(
        word
        for _, word in words
    )


def calculate_relevance(
    title,
    abstract
):

    text = (
        f"{title} {abstract}"
    ).lower()

    score = 0

    keywords = {

        "work disengagement": 30,
        "employee disengagement": 25,
        "job disengagement": 25,
        "withdrawal": 15,
        "burnout": 10,
        "quiet quitting": 20,
        "engagement": 5,

        "psychological safety": 5,
        "leadership": 5,
        "turnover": 5
    }

    for term, value in keywords.items():

        if term in text:

            score += value

    return min(score, 100)


def search_openalex(
    keyword,
    per_page=50
):

    params = {
        "search": keyword,
        "per-page": per_page
    }

    response = requests.get(
        BASE_URL,
        params=params
    )

    if response.status_code != 200:

        print(
            f"Error searching {keyword}"
        )

        return []

    data = response.json()

    papers = []

    for item in data.get(
        "results",
        []
    ):

        title = item.get(
            "title",
            ""
        )

        year = item.get(
            "publication_year"
        )

        doi = item.get(
            "doi"
        )

        journal = ""

        if item.get(
            "primary_location"
        ):

            source = item[
                "primary_location"
            ].get(
                "source"
            )

            if source:

                journal = source.get(
                    "display_name",
                    ""
                )

        authors = []

        for a in item.get(
            "authorships",
            []
        ):

            author = a.get(
                "author",
                {}
            )

            authors.append(
                author.get(
                    "display_name",
                    ""
                )
            )

        abstract_text = reconstruct_abstract(
            item.get(
                "abstract_inverted_index",
                {}
            )
        )

        relevance_score = (
            calculate_relevance(
                title,
                abstract_text
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

        if item.get(
            "primary_location"
        ):

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

            "abstract": abstract_text,

            "relevance_score":
                relevance_score,

            "citation_count":
                item.get(
                    "cited_by_count",
                    0
                ),

            "access_type":
                access_type,

            "pdf_available":
                pdf_available,

            "pdf_link":
                pdf_link,

            "repository_link":
                landing_page,

            "publisher_link":
                landing_page,

            "keyword":
                keyword,

            "source":
                "OpenAlex"
        })

    return papers
