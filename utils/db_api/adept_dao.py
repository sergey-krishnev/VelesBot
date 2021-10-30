from utils.db_api import db


def add_adept(name, description):
    inserted_row_id = db.insert("adepts", {
        "name": name,
        "description": description
    })
    return inserted_row_id


def get_adept_by_id(adept_id):
    result = None
    adepts = db.fetchall_with_filter("adepts", ["name"], [f"id={adept_id}"])
    if adepts:
        result = adepts[0].get("name")
    return result
