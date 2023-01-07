# Author ph
# Company NKCS
# created at 2023/1/2  7:22 PM

import pymysql
from pymysql.constants import CLIENT
from config import config

host = config['database']['host']
user = config['database']['user']
passwd = config['database']['password']
database = config['database']['database']


# 检查教师是否重复注册
def check_teacher_repeated(account):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd,
                           database=database, charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'SELECT * FROM Teacher WHERE account = \'' + account + '\';'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(res) > 0:
        return True
    else:
        return False


def teacher_register(account, password):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'INSERT INTO Teacher VALUES(\'' + account + '\', \'' + password + '\');'

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()


def check_student_repeated(account):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'SELECT * FROM Student WHERE account = \'' + account + '\';'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(res) > 0:
        return True
    else:
        return False


def student_register(account, password, name):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'INSERT INTO Student VALUES(\'' + account + '\', \'' + password + '\',\'' + name + '\');'

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()


def lesson_id_insert(lesson_id, account, lesson_date, lesson_info, lesson_period):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'INSERT INTO Teacher_Lesson VALUES(\'' + lesson_id + '\', \'' + account + '\',\'' \
          + lesson_date + '\',\'' + lesson_info + '\', ' + lesson_period + ');'

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()


def check_lesson_id(lesson_id):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'SELECT * FROM Teacher_Lesson WHERE lesson_id = \'' + lesson_id + '\';'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(res) > 0:
        return True
    else:
        return False


def student_add_lesson(account, lesson_id):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'INSERT INTO Student_Lesson VALUES(\'' + lesson_id + '\', \'' + account + \
          '\', default, default, default, default, default, default, default, default, default);'

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()


def student_post_data(account, lesson_id, sleep_count, sleep_time, talk_count,
                      talk_time, pry_count, pry_time, absence_count, absence_time,
                      total_time):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'UPDATE Student_Lesson SET sleep_count = ' + sleep_count + ', sleep_time = ' + sleep_time \
          + ', talk_count = ' + talk_count + ', talk_time = ' + talk_time + ', pry_count = ' + pry_count \
          + ', pry_time = ' + pry_time + ', absence_count = ' + absence_count + ', absence_time = ' \
          + absence_time + ', total_time = ' + total_time \
          + ' WHERE lesson_id = \'' + lesson_id + '\' AND student_id = \'' + account + '\';'

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()


def teacher_get_lesson(account):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'SELECT lesson_id, lesson_date, lesson_period, lesson_info FROM Teacher_Lesson ' \
          'WHERE teacher_id = \'' + account + '\';'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res


def teacher_get_record(lesson_id):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    sql = 'SELECT name, sleep_count, sleep_time, talk_count, talk_time, ' \
          'pry_count, pry_time, absence_count, absence_time, total_time, lesson_period ' \
          'FROM Student_Lesson, Teacher_Lesson, Student WHERE Student_Lesson.lesson_id = \'' + lesson_id + \
          '\' and student_id = account and Teacher_Lesson.lesson_id = Student_Lesson.lesson_id;'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res


def student_get_record(account):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()

    sql = 'SELECT lesson_date, lesson_info, sleep_count, sleep_time, talk_count, talk_time, ' \
          'pry_count, pry_time, absence_count, absence_time, total_time, lesson_period ' \
          'FROM Student_Lesson, Teacher_Lesson WHERE student_id = \'' + account + \
          '\' AND Student_Lesson.lesson_id = Teacher_Lesson.lesson_id;'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res


# 检测学生重复参与课程
def check_start_lesson_repeat(lesson_id, account):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()

    sql = 'SELECT * FROM STUDENT_LESSON WHERE lesson_id = \'' + lesson_id \
          + '\' and student_id = \'' + account + '\';'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(res) > 0:
        return True
    else:
        return False


def teacher_login(account, password):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()

    sql = 'SELECT * FROM TEACHER WHERE account = \'' + account \
          + '\' AND keyword = \'' + password + '\';'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(res) > 0:
        return True
    else:
        return False


def student_login(account, password):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()

    sql = 'SELECT * FROM STUDENT WHERE account = \'' + account \
          + '\' AND keyword = \'' + password + '\';'

    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(res) > 0:
        return True
    else:
        return False


def lesson_belong_teacher(account, lesson_id):
    # 经查阅资料发现，pymysql在8.0版本后默认不执行多条语句，通过设置client_flag参数以执行多条sql语句
    conn = pymysql.connect(host=host, user=user, password=passwd, database=database,
                           charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()

    sql = 'SELECT * FROM TEACHER_LESSON WHERE teacher_id = \'' + account \
          + '\' AND lesson_id = \'' + lesson_id + '\';'
    cursor.execute(sql)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(res) == 1:
        return True
    else:
        return False
