from utils.constants import MAX_ENERGY
from utils.db_api import db
from utils.db_api.postgres_db import QuickConnection


def register_user(user_id):
    db.insert("users", {"id": user_id})


def get_user_by_id(user_id):
    result = None
    questions = db.fetchall_with_filter("users", ["id", "coin", "energy", "rank"], [f"id={user_id}"])
    if questions:
        result = questions[0]
    return result


def spend_energy(user_id, energy):
    with QuickConnection() as cursor:
        cursor.execute(f"UPDATE users SET energy = energy - %s WHERE id= %s", (str(energy), str(user_id)))


def restore_energy_using_coins(user_id, coin):
    with QuickConnection() as cursor:
        cursor.execute(f"UPDATE users SET energy = %s, coin = coin - %s WHERE id= %s", (str(MAX_ENERGY), str(coin),
                                                                                        str(user_id)))


def add_coins(user_id, coin):
    with QuickConnection() as cursor:
        cursor.execute(f"UPDATE users SET coin = coin + %s WHERE id= %s", (str(coin), str(user_id)))


def spend_coins(user_id, coin):
    with QuickConnection() as cursor:
        cursor.execute(f"UPDATE users SET coin = coin - %s WHERE id= %s", (str(coin), str(user_id)))
