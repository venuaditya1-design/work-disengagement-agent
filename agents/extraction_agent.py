THEORIES = {

    "job demands-resources": "JD-R",
    "jd-r": "JD-R",

    "conservation of resources": "COR",

    "social exchange": "SET",

    "self-determination": "SDT",

    "affective events": "AET"
}


METHODS = {

    "pls-sem": "PLS-SEM",

    "smartpls": "PLS-SEM",

    "structural equation modeling": "SEM",

    "structural equation modelling": "SEM",

    "amos": "CB-SEM",

    "regression": "Regression",

    "cross-sectional": "Cross-Sectional",

    "longitudinal": "Longitudinal"
}


INDUSTRIES = {

    "hospital": "Healthcare",
    "nurse": "Healthcare",

    "teacher": "Education",
    "university": "Education",

    "bank": "Banking",

    "software": "IT",

    "information technology": "IT"
}


COUNTRIES = [

    "india",
    "pakistan",
    "china",
    "bangladesh",
    "sri lanka",
    "united states",
    "usa",
    "uk",
    "united kingdom",
    "australia",
    "canada"
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
