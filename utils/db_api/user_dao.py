from utils.db_api import db


def register_user(user_id):
    db.insert("users", {"id": user_id})


def get_user_by_id(user_id):
    result = None
    questions = db.fetchall_with_filter("users", ["id", "coin", "energy", "rank"], [f"id={user_id}"])
    if questions:
        result = questions[0]
    return result