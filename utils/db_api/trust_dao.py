from utils.db_api import db


def is_new_account(user_id):
    return len(db.fetchall_with_filter("trust", ["id"], [f"user_id={user_id}"])) == 0


def add_trust(user_id, adept_id):
    inserted_row_id = db.insert("trust", {
        "user_id": user_id,
        "adept_id": adept_id,
        "trust_level": 1,
        "points": 0
    })
    return inserted_row_id


def is_not_all_adepts_opened(user_id):
    trust_len = len(db.fetchall_with_filter("trust", ["id"], [f"user_id={user_id}"]))
    adept_len = len(db.fetchall("adepts", ["id"]))
    return trust_len != adept_len
