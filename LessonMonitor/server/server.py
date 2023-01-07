# Author ph
# Company NKCS
# created at 2023/1/2  5:48 PM

import random, datetime
from flask import Flask, request, jsonify
from database import *
from config import config
from gevent import pywsgi

app = Flask(__name__)


@app.route('/teacher/login')
def func0():
    account = request.values.get('account')
    password = request.values.get('password')

    if teacher_login(account, password):
        return 'TEACHER_LOGIN_SUCCESS'
    else:
        return 'TEACHER_LOGIN_FAIL'


@app.route('/teacher/register')
def func1():
    account = request.values.get('account')
    password = request.values.get('password')

    if check_teacher_repeated(account):
        return 'TEACHER_ACCOUNT_REPEATED'

    teacher_register(account, password)
    return 'TEACHER_REGISTER_SUCCESS'


@app.route('/teacher/lesson')
def func2():
    account = request.values.get('account')
    now = str(datetime.datetime.now())
    info = request.values.get('info')
    period = request.values.get('period')

    lesson_id = ''
    for i in range(32):
        num = random.randint(0, 9)
        lesson_id = lesson_id + str(num)

    lesson_id_insert(lesson_id, account, now, info, period)

    return lesson_id


@app.route('/teacher/get/lesson')
def func3():
    account = request.values.get('account')
    res = teacher_get_lesson(account)
    return jsonify(list(res))


@app.route('/teacher/get/record')
def func4():
    account = request.values.get('account')
    lesson_id = request.values.get('lesson_id')

    if not check_lesson_id(lesson_id):
        return 'LESSON_ID_NOT_EXISTS'

    if not lesson_belong_teacher(account, lesson_id):
        return 'LESSON_NOT_BELONG_TEACHER'

    res = teacher_get_record(lesson_id)
    print(res)
    return jsonify(list(res))


@app.route('/student/register')
def func5():
    account = request.values.get('account')
    password = request.values.get('password')
    name = request.values.get('name')

    if check_student_repeated(account):
        return 'STUDENT_ACCOUNT_REPEATED'

    student_register(account, password, name)
    return 'STUDENT_REGISTER_SUCCESS'


@app.route('/student/lesson')
def func6():
    account = request.values.get('account')
    lesson_id = request.values.get('lesson_id')

    if not check_lesson_id(lesson_id):
        return 'LESSON_ID_NOT_EXISTS'

    if check_start_lesson_repeat(lesson_id, account):
        return 'JOIN_LESSON_REPEAT'

    student_add_lesson(account, lesson_id)
    return 'STUDENT_JOIN_LESSON'


@app.route('/student/postdata')
def func7():
    account = request.values.get('account')
    lesson_id = request.values.get('lesson_id')
    sleep_count = request.values.get('sleep_count')
    sleep_time = request.values.get('sleep_time')
    talk_count = request.values.get('talk_count')
    talk_time = request.values.get('talk_time')
    pry_count = request.values.get('pry_count')
    pry_time = request.values.get('pry_time')
    absence_count = request.values.get('absence_count')
    absence_time = request.values.get('absence_time')
    total_time = request.values.get('total_time')

    student_post_data(account, lesson_id, sleep_count, sleep_time, talk_count, talk_time,
                      pry_count, pry_time, absence_count, absence_time, total_time)
    return 'STUDENT_POST_DATA'


@app.route('/student/get/record')
def func8():
    account = request.values.get('account')
    res = student_get_record(account)

    return jsonify(list(res))


@app.route('/student/login')
def func9():
    account = request.values.get('account')
    password = request.values.get('password')

    if student_login(account, password):
        return 'STUDENT_LOGIN_SUCCESS'
    else:
        return 'STUDENT_LOGIN_FAIL'


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False

    host = config['server']['host']
    port = config['server']['port']
    server = pywsgi.WSGIServer((host, port), app)
    server.serve_forever()
