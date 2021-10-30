from utils.db_api import db
import random


def add_theme(theme_name, adept_id):
    inserted_row_id = db.insert("themes", {
        "name": theme_name,
        "adept_id": adept_id
    })
    return inserted_row_id


def get_random_theme_by_adept(adept_id):
    result = None
    themes = db.fetchall_with_filter("themes", ["id"], [f"adept_id={adept_id}"])
    if themes:
        result = random.choice(themes).get("id")
    return result