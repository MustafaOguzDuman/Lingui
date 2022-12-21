import datetime
import random
import os
import psycopg2
import config

from flask import Flask, session, app, request, jsonify

app = Flask(__name__)
config.set_values()


# run the flask app from terminal with this command:
# FLASK_APP=main.py flask run


def connect():
    conn = psycopg2.connect(
        host=os.getenv('URL'),
        database=os.getenv('DATABASE_NAME'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD')
    )

    return conn


connection = connect()
cursor = connection.cursor()


@app.route('/')
def index():
    return 'Hello World'


@app.route('/check-answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    user_id = data['user_id']
    word_id = data['word_id']
    answer_is_correct = data['answer_is_correct']

    if answer_is_correct:
        correct_answer(user_id, word_id)
    else:
        incorrect_answer(user_id, word_id)

    return jsonify({'success': True}), 200


def correct_answer(user_id, word_id):
    # TODO: database'den word_id ve user_id'ye karşılık gelen word'ün strength'ine bak
    # TODO: strength'i ve due date'i update'le
    # TODO: yeni strength ve due date'i database'ye geri yaz

    word_strength = get_word_strength(user_id, word_id) + 1

    # card with more than 7 strength is removed from the list
    if word_strength > 7:
        remove_word_from_list(user_id, word_id)
    else:
        due_date = calculate_due_date(user_id, word_id, word_strength)
        print("in correct answer")
        print(due_date)
        print(word_strength)
        update_database(user_id, word_id, word_strength, due_date)


def incorrect_answer(user_id, word_id):
    # TODO: database'den word_id ve user_id'ye karşılık gelen word'ün strength'ine bak
    # TODO: strength'i ve due date'i update'le
    # TODO: yeni strength ve due date'i database'ye geri yaz

    word_strength = 1

    due_date = calculate_due_date(user_id, word_id, word_strength)
    print(due_date - datetime.datetime.now())
    update_database(user_id, word_id, word_strength, due_date)


def calculate_due_date(user_id, word_id, word_strength):
    MINS_IN_DAY = 1440

    default_mins = get_default_mins(user_id)
    ease_factor = get_ease_factor(user_id)

    if word_strength <= len(default_mins):
        added_mins = default_mins[word_strength - 1]
        return datetime.datetime.now() + datetime.timedelta(minutes=fuzz(added_mins))
    else:
        days_past_after_due = (datetime.datetime.now() - get_due_date(user_id, word_id)).days

        added_days = pow(ease_factor, word_strength - len(default_mins) - 1) + days_past_after_due / 2
        added_mins = added_days * MINS_IN_DAY

        return datetime.datetime.now() + datetime.timedelta(minutes=fuzz(added_mins))


def fuzz(number):
    return number * (random.randint(100, 124) / 100)


def word_is_due(user_id, word_id):
    return get_due_date(user_id, word_id) <= datetime.datetime.now()


def get_due_date(user_id, word_id):
    cursor.execute("SELECT due_date FROM word_strength_due_list WHERE user_id = %s AND word_id = %s",
                   (user_id, word_id))
    due_date = cursor.fetchone()[0]
    return due_date


def get_default_mins(user_id):
    # TODO: get mins from database from the user's settings
    return [1, 10]


def get_ease_factor(user_id):
    # TODO: get ease factor from the user
    return 2.5


def get_word_strength(user_id, word_id):
    # get word strength from database
    cursor.execute("SELECT strength FROM word_strength_due_list WHERE user_id = %s AND word_id = %s",
                   (user_id, word_id))
    strength = cursor.fetchone()[0]
    return strength


def update_database(user_id, word_id, word_strength, due_date):
    # update word strength and due date in database
    cursor.execute("UPDATE word_strength_due_list SET strength = %s, due_date = %s WHERE user_id = %s AND word_id = %s",
                   (word_strength, due_date, user_id, word_id))

    connection.commit()


def remove_word_from_list(user_id, word_id):
    cursor.execute("DELETE FROM word_strength_due_list WHERE user_id = %s AND word_id = %s",
                   (user_id, word_id))
    connection.commit()


@app.route('/add-word-to-user', methods=['POST'])
def add_word_to_user():
    json = request.get_json()
    user_id = json['user_id']
    word_id = json['word_id']

    # TODO: check if already exists in database

    word_strength = 1
    due_date = datetime.datetime.now() + datetime.timedelta(minutes=1)

    cursor.execute("INSERT INTO word_strength_due_list (user_id, word_id, strength, due_date) VALUES (%s, %s, %s, %s)",
                   (user_id, word_id, word_strength, due_date))

    connection.commit()

    return jsonify({'success': True}), 200


if __name__ == '__main__':
    app.run(debug=True)
