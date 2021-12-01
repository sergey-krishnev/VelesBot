from utils.db_api import db
from utils.db_api.postgres_db import QuickConnection


def add_checkpoint(connection_id, user_id):
    inserted_row_id = db.insert("checkpoints", {
        "connection_id": connection_id,
        "user_id": user_id,
    })
    return inserted_row_id


def remove_checkpoint(user_id):
    with QuickConnection() as cursor:
        cursor.execute(f"delete from checkpoints where user_id={user_id}")


def update_checkpoint_to_solve(connection_id):
    with QuickConnection() as cursor:
        cursor.execute("UPDATE checkpoints SET solved=TRUE WHERE connection_id= %s", (str(connection_id),))


def update_checkpoint_to_unsolve(connection_id, checkpoint_id):
    with QuickConnection() as cursor:
        cursor.execute("UPDATE checkpoints SET solved=FALSE, connection_id=%s WHERE id= %s", (str(connection_id),
                                                                                              str(checkpoint_id)))


def finish_dialog(connection_id):
    with QuickConnection() as cursor:
        cursor.execute("UPDATE checkpoints SET finished=TRUE WHERE connection_id= %s", (str(connection_id),))


def is_finished_dialog(user_id):
    return len(db.fetchall_with_filter("checkpoints", ["id"], [f"user_id={user_id}", "finished=TRUE"])) != 0


def get_checkpoint_by_user_id(user_id):
    result = None
    checkpoints = db.fetchall_with_filter("checkpoints", ["id", "connection_id"], [f"user_id={user_id}"])
    if checkpoints:
        result = checkpoints[0]
    return result


def has_not_checkpoint(user_id):
    return len(db.fetchall_with_filter("checkpoints", ["id"], [f"user_id={user_id}"])) == 0


def is_not_solved_checkpoint(user_id):
    return len(db.fetchall_with_filter("checkpoints", ["id"], [f"user_id={user_id}", "solved=FALSE"])) != 0
