THEORIES = {

    # JD-R

    "job demands-resources": "JD-R",
    "jd-r": "JD-R",
    "job resources": "JD-R",
    "job demands": "JD-R",
    "demands-resources": "JD-R",

    # COR

    "conservation of resources": "COR",
    "resource loss": "COR",
    "resource gain": "COR",

    # SET

    "social exchange": "SET",
    "exchange relationship": "SET",

    # SDT

    "self-determination": "SDT",
    "self determination": "SDT",

    # AET

    "affective events": "AET",
    "affective event": "AET"
}


METHODS = {

    "pls-sem": "PLS-SEM",
    "smartpls": "PLS-SEM",
    "partial least squares": "PLS-SEM",

    "structural equation modeling": "SEM",
    "structural equation modelling": "SEM",

    "amos": "CB-SEM",

    "regression": "Regression",

    "cross-sectional": "Cross-Sectional",

    "longitudinal": "Longitudinal",

    "survey": "Survey"
}


INDUSTRIES = {

    # Healthcare

    "hospital": "Healthcare",
    "nurse": "Healthcare",
    "doctor": "Healthcare",
    "physician": "Healthcare",

    # Education

    "teacher": "Education",
    "faculty": "Education",
    "lecturer": "Education",
    "university": "Education",
    "academic": "Education",

    # Banking

    "bank": "Banking",
    "banking": "Banking",

    # IT

    "software": "IT",
    "information technology": "IT",
    "it sector": "IT",

    # Hospitality

    "hotel": "Hospitality",
    "hospitality": "Hospitality",

    # Manufacturing

    "manufacturing": "Manufacturing",

    # Public sector

    "public sector": "Public Sector",
    "government": "Public Sector"
}


COUNTRIES = [

    "india",
    "pakistan",
    "china",
    "bangladesh",
    "sri lanka",
    "nepal",

    "united states",
    "usa",
    "canada",

    "united kingdom",
    "uk",

    "australia",

    "germany",
    "france",
    "italy",
    "spain",

    "saudi arabia",
    "uae",
    "qatar",

    "malaysia",
    "singapore",
    "indonesia",
    "thailand",

    "south africa",
    "nigeria"
]


def extract_research_data(
    title,
    abstract
):

    text = (
        f"{title} {abstract}"
    ).lower()

    theory_primary = ""

    for key, value in THEORIES.items():

        if key in text:

            theory_primary = value

            break

    method = ""

    for key, value in METHODS.items():

        if key in text:

            method = value

            break

    industry = ""

    for key, value in INDUSTRIES.items():

        if key in text:

            industry = value

            break

    country = ""

    for item in COUNTRIES:

        if item in text:

            country = item.title()

            break

    return {

        "theory_primary":
            theory_primary,

        "method":
            method,

        "industry":
            industry,

        "country":
            country
    }
