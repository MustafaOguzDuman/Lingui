import datetime
import random

from flask import session, app


@app.route('/correct')
def correct_answer(word_id, user_id):
    # TODO: database'den word_id ve user_id'ye karşılık gelen word'ün strength'ine bak
    # TODO: strength'i ve due date'i update'le
    # TODO: yeni strength ve due date'i database'ye geri yaz

    word_strength = get_word_strength(word_id, user_id)
    due_date = get_due_date(word_id, user_id)

    word_strength += 1

    if word_strength == 7:
        remove_word_from_list(word_id, user_id)
    else:
        due_date = calculate_due_date(user_id, word_id, word_strength)
        update_database(user_id, word_id, word_strength, due_date)


def incorrect_answer(word_id, user_id):
    # TODO: database'den word_id ve user_id'ye karşılık gelen word'ün strength'ine bak
    # TODO: strength'i ve due date'i update'le
    # TODO: yeni strength ve due date'i database'ye geri yaz

    word_strength = get_word_strength(word_id, user_id)
    due_date = get_due_date(word_id, user_id)

    word_strength = 1

    due_date = calculate_due_date(user_id, word_id, word_strength)
    update_database(user_id, word_id, word_strength, due_date)


# returns due date
def calculate_due_date(user_id, word_id, word_strength):
    MINS_IN_DAY = 1440

    default_mins = get_default_mins(user_id)
    ease_factor = get_ease_factor(user_id)

    # first three intervals are preset
    if word_strength < 3:
        added_mins = default_mins[word_strength]
    else:
        previous_due_date = pow(ease_factor, word_strength - 3)
        days_past_after_due = (datetime.datetime.now() - get_due_date(word_id, user_id)) // MINS_IN_DAY
        added_mins = (previous_due_date + days_past_after_due / 2) * get_ease_factor(user_id)

    return datetime.datetime.now() + datetime.timedelta(minutes=added_mins * (random.randint(0, 25) / 100))


def word_is_due(word_id, user_id):
    return get_due_date(word_id, user_id) <= datetime.datetime.now()


def get_due_date(word_id, user_id):
    pass


def get_default_mins(user_id):
    # TODO: get mins from database from the user's settings
    return [1, 10, 1440]


def get_ease_factor(user_id):
    # TODO: get ease factor from the user
    pass


def get_word_strength(user_id, word_id):
    pass


def update_database(user_id, word_id, word_strength, due_date):
    pass


def remove_word_from_list(user_id, word_id):
    pass