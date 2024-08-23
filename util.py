import json
from re import search


def get_category(description: str):
    """_summary_

    Args:
        description (str): transaction description

    Returns:
        str: category of the transaction description
    """
    description = description.lower()
    categories = json.load(open("./category.json", encoding="utf-8"))
    category = "other".capitalize()
    for i in categories:
        for j in categories[i]:
            if search(j.lower(), description):
                category = i.capitalize()
                return category
    return category
