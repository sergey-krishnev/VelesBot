from utils.db_api import db


def get_dialog_detailed(connection_id) -> list:
    dialog = []
    connection = db.fetchall_with_filter("connections", ["prev_question_id", "answer_id"], [f"id={connection_id}"])[0]
    prev_question_id = connection.get("prev_question_id")
    consequence_ids = []
    question_ids = []
    answer_ids = []
    question_dict = {}
    answer_dict = {}
    consequence_ids.append(connection.get("answer_id"))
    consequence_ids.append(prev_question_id)
    question_ids.append(prev_question_id)
    answer_ids.append(connection.get("answer_id"))
    while True:

        prev_connections = db.fetchall_with_filter("connections", ["prev_question_id", "answer_id"],
                                                   [f"next_question_id={prev_question_id}"])
        if not prev_connections:
            break
        prev_connection = prev_connections[0]
        prev_question_id = prev_connection.get("prev_question_id")
        question_ids.append(prev_question_id)
        consequence_ids.append(prev_connection.get("answer_id"))
        consequence_ids.append(prev_question_id)
        answer_ids.append(prev_connection.get("answer_id"))

    questions = db.fetchall_with_filter("questions", ["id", "name"],
                                        [f"id in {tuple(question_ids)}"
                                         if len(question_ids) > 1
                                         else f"id={question_ids[0]}"])
    answers = db.fetchall_with_filter("answers", ["id", "name"],
                                      [f"id in {tuple(answer_ids)}"
                                       if len(answer_ids) > 1
                                       else f"id={answer_ids[0]}"])
    for question in questions:
        question_dict[question.get("id")] = question.get("name")
    for answer in answers:
        answer_dict[answer.get("id")] = answer.get("name")

    is_question = True
    is_answer = False
    for i in range(len(consequence_ids) - 1, -1, -1):
        if is_question:
            dialog.append(question_dict.get(consequence_ids[i]))
            is_answer = True
            is_question = False
            continue
        if is_answer:
            dialog.append(answer_dict.get(consequence_ids[i]))
            is_question = True
            is_answer = False

    return dialog

