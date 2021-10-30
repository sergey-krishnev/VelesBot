from utils.db_api import db


def add_suggestion(suggestion_name, user_id):
    inserted_row_id = db.insert("suggestions", {
        "name": suggestion_name,
        "user_id": user_id
    })
    return inserted_row_id


def get_suggestion_by_id(suggestion_id):
    result = None
    suggestions = db.fetchall_with_filter("suggestions", ["name"], [f"id={suggestion_id}"])
    if suggestions:
        result = suggestions[0].get("name")
    return result
