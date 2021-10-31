from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_data import open_menu_callback
from utils.db_api import db


def get_active_dialogs():
    # TODO Доработать вывод активных диалогов
    question_dict = {}
    answer_dict = {}
    checkpoints = db.fetchall_with_filter("checkpoints", ["connection_id"], [f"solved=0"])
    if len(checkpoints) == 0:
        return None
    connection_ids = tuple([c["connection_id"] for c in checkpoints])
    connections = db.fetchall_with_filter("connections", ["id", "prev_question_id", "answer_id"],
                                          [f"id in {connection_ids}"
                                           if len(connection_ids) > 1
                                           else f"id={connection_ids[0]}", "answer_id is not null"])

    prev_question_ids = tuple([c["prev_question_id"] for c in connections])
    questions = db.fetchall_with_filter("questions", ["id", "name"],
                                        [f"id in {prev_question_ids}"
                                         if len(prev_question_ids) > 1
                                         else f"id={prev_question_ids[0]}"])

    answer_ids = tuple([c["answer_id"] for c in connections])
    answers = db.fetchall_with_filter("answers", ["id", "name"],
                                      [f"id in {answer_ids}"
                                       if len(answer_ids) > 1
                                       else f"id={answer_ids[0]}"])

    for question in questions:
        question_dict[question.get("id")] = question.get("name")
    for answer in answers:
        answer_dict[answer.get("id")] = answer.get("name")
    inline = []
    for connection in connections:
        question = question_dict.get(connection.get("prev_question_id"))
        answer = answer_dict.get(connection.get("answer_id"))
        inline.append([InlineKeyboardButton(text=f"Вопрос: '{question}' Ответ: '{answer}' ",
                                            callback_data=open_menu_callback.new(menu="dialog_detailed",
                                                                                 id=connection.get("id")))])
    return InlineKeyboardMarkup(inline_keyboard=inline)
