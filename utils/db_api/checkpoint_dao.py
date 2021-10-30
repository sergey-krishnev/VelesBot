from utils.db_api import db


def add_checkpoint(connection_id, user_id):
    inserted_row_id = db.insert("checkpoints", {
        "connection_id": connection_id,
        "user_id": user_id,
    })
    return inserted_row_id


def update_checkpoint_to_solve(connection_id):
    cursor = db.get_cursor()
    cursor.execute("UPDATE checkpoints SET solved=1 WHERE connection_id= ?", (connection_id,))
    cursor.close()


def update_checkpoint_to_unsolve(connection_id, checkpoint_id):
    cursor = db.get_cursor()
    cursor.execute("UPDATE checkpoints SET solved=0, connection_id=? WHERE id= ?", (connection_id, checkpoint_id))
    cursor.close()


def get_checkpoint_by_user_id(user_id):
    result = None
    checkpoints = db.fetchall_with_filter("checkpoints", ["id", "connection_id"], [f"user_id={user_id}"])
    if checkpoints:
        result = checkpoints[0]
    return result


def has_not_checkpoint(user_id):
    return len(db.fetchall_with_filter("checkpoints", ["id"], [f"user_id={user_id}"])) == 0


def is_not_solved_checkpoint(user_id):
    return len(db.fetchall_with_filter("checkpoints", ["id"], [f"user_id={user_id}", "solved=0"])) != 0
