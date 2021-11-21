import random

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


def get_random_unowned_adept_id(user_id):
    opened_adepts_ids = db.fetchall_with_filter("trust", ["adept_id"], [f"user_id={user_id}"])
    if opened_adepts_ids:
        opened_adepts_ids = tuple([c["adept_id"] for c in opened_adepts_ids])
        adepts = db.fetchall_with_filter("adepts", ["id"], [f"id not in {tuple(opened_adepts_ids)}"
                                                            if len(opened_adepts_ids) > 1
                                                            else f"id<>{opened_adepts_ids[0]}"])
    else:
        adepts = db.fetchall("adepts", ["id"])
    return random.choice(adepts).get("id")
