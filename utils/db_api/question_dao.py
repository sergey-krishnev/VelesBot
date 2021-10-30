import random

from utils.db_api import db


def add_question(question_name, theme_id):
    inserted_row_id = db.insert("questions", {
        "name": question_name,
        "theme_id": theme_id
    })
    return inserted_row_id


def get_question_name_by_id(question_id):
    result = None
    questions = db.fetchall_with_filter("questions", ["name"], [f"id={question_id}"])
    if questions:
        result = questions[0].get("name")
    return result


def get_question_by_id(question_id):
    result = None
    questions = db.fetchall_with_filter("questions", ["name"], [f"id={question_id}"])
    if questions:
        result = questions[0]
    return result


def add_question_without_theme(question_name):
    inserted_row_id = db.insert("questions", {
        "name": question_name
    })
    return inserted_row_id


def get_random_question_by_theme(theme_id):
    result = None
    questions = db.fetchall_with_filter("questions", ["id", "name"], [f"theme_id={theme_id}"])
    if questions:
        result = random.choice(questions)
    return result
