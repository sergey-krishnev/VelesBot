from utils.db_api import db


def add_answer(answer_name):
    inserted_row_id = db.insert("answers", {
        "name": answer_name
    })
    return inserted_row_id
