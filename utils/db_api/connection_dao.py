from utils.db_api import db


def add_connection(prev_question_id):
    inserted_row_id = db.insert("connections", {
        "prev_question_id": prev_question_id
    })
    return inserted_row_id


def update_connection_with_answer(connection_id, answer_id):
    cursor = db.get_cursor()
    cursor.execute("UPDATE connections SET answer_id = ? WHERE id= ?", (answer_id, connection_id))
    cursor.close()


def update_connection_with_next_question(connection_id, next_question_id):
    cursor = db.get_cursor()
    cursor.execute("UPDATE connections SET next_question_id = ? WHERE id= ?", (next_question_id, connection_id))
    cursor.close()


def get_next_question_by_id(connection_id):
    result = None
    connections = db.fetchall_with_filter("connections", ["next_question_id"], [f"id={connection_id}"])
    if connections:
        result = connections[0].get("next_question_id")
    return result


def get_prev_question_by_id(connection_id):
    result = None
    connections = db.fetchall_with_filter("connections", ["prev_question_id"], [f"id={connection_id}"])
    if connections:
        result = connections[0].get("prev_question_id")
    return result


def get_prev_connection_by_next_question_id(prev_question_id):
    result = None
    prev_connections = db.fetchall_with_filter("connections", ["id", "prev_question_id", "answer_id"],
                                               [f"next_question_id={prev_question_id}"])
    if prev_connections:
        result = prev_connections[0]
    return result
