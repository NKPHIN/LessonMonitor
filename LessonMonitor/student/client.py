# Author ph
# Company NKCS
# created at 2023/1/2  5:48 PM

# 导入requests包
import requests
from config import config

# 根路径
root = 'http://' + config['server']['host'] + ':' + str(config['server']['port'])


def login_teacher(account, password):
    """
        教师登录
        :param account: 账号名
        :param password: 密码
        :return: 登录状态
        :return 'TEACHER_LOGIN_SUCCESS': 登录成功
        :return 'TEACHER_LOGIN_FAIL': 登录失败
    """
    url = root + '/teacher/login'
    params = {'account': account, 'password': password}
    res = requests.get(url=url, params=params)

    print('response', res.text)
    return res.text


def register_teacher(account, password):
    """
        向服务器注册教师账号
        :param account: 账号名, 不可重复
        :param password: 密码

        :return  一个字符串表示注册状态
        :return 'TEACHER_ACCOUNT_REPEATED': 账号名已存在
        :return 'TEACHER_REGISTER_SUCCESS': 注册成功
    """
    url = root + '/teacher/register'
    params = {'account': account, 'password': password}
    res = requests.get(url=url, params=params)

    print('response', res.text)
    return res.text


def register_student(account, password, name):
    """
        向服务器注册学生账号
        :param account: 账号名, 不可重复
        :param password: 密码
        :param name: 学生姓名，方便教师统计

        :return  一个字符串表示注册状态
        :return 'STUDENT_ACCOUNT_REPEATED': 账号名已存在
        :return 'STUDENT_REGISTER_SUCCESS': 注册成功
    """
    url = root + '/student/register'
    params = {'account': account, 'password': password, 'name': name}
    res = requests.get(url=url, params=params)

    print('response', res.text)
    return res.text


def login_student(account, password):
    """
        学生登录
        :param account: 账号名
        :param password: 密码
        :return: 登录状态
        :return 'STUDENT_LOGIN_SUCCESS': 登录成功
        :return 'STUDENT_LOGIN_FAIL': 登录失败
    """
    url = root + '/student/login'
    params = {'account': account, 'password': password}
    res = requests.get(url=url, params=params)

    print('response', res.text)
    return res.text


def request_lesson_id(account, period, info=''):
    """
        教师向服务器申请一个课程号
        :param period: 上课时长
        :param account: 教师账号
        :param info: 附带的课程信息，例如'第一堂课'， 可为空

        :return  一个32位的随机数字串
    """
    url = root + '/teacher/lesson'
    params = {'account': account, 'info': info, 'period': period}
    res = requests.get(url=url, params=params)

    print('response', res.text)
    return res.text


def student_add_lesson(account, lesson_id):
    """
        学生根据老师提供的课程号加入课程，开始录屏
        :param account: 学生账号
        :param lesson_id: 课程号

        :return  申请状态
        :return 'LESSON_ID_NOT_EXISTS': 课程号不存在
        :return 'JOIN_LESSON_REPEAT': 重复加入课程
        :return 'STUDENT_JOIN_LESSON': 加入成功
    """
    url = root + '/student/lesson'
    params = {'account': account, 'lesson_id': lesson_id}
    res = requests.get(url=url, params=params)

    print('response', res.text)
    return res.text


def student_post_data(account, lesson_id,
                      sleep_count=0, sleep_time=0,
                      talk_count=0, talk_time=0,
                      pry_count=0, pry_time=0,
                      absence_count=0, absence_time=0,
                      total_time=0):
    """
        学生端将课程表现记录上传至服务器
        :param account: 学生账号
        :param lesson_id: 课程号
        :param sleep_count: 瞌睡次数
        :param sleep_time: 总瞌睡时间
        :param talk_count: 讲话次数
        :param talk_time: 讲话时间
        :param pry_count: 东张西望次数
        :param pry_time: 东张西望时间
        :param absence_count: 缺席次数
        :param absence_time: 总缺席时间
        :param total_time: 总录制时间

        :return 'STUDENT_POST_DATA': 上传成功

        注意本函数不提供学生账号和课程号的有效性检验
        建议在成功加入课程开始录屏后，由客户端暂存账
        号和课程号信息，结束录屏后再调用本函数
    """
    url = root + '/student/postdata'
    params = {
        'account': account,
        'lesson_id': lesson_id,
        'sleep_count': sleep_count,
        'sleep_time': sleep_time,
        'talk_count': talk_count,
        'talk_time': talk_time,
        'pry_count': pry_count,
        'pry_time': pry_time,
        'absence_count': absence_count,
        'absence_time': absence_time,
        'total_time': total_time
    }
    res = requests.get(url=url, params=params)

    print("response:", res.text)
    return res.text


def teacher_get_lesson(account):
    """
        教师查询历史授课记录
        :param account: 教师账号

        :return 返回一个列表，包含由该教师创建的所有课程号
    """
    url = root + '/teacher/get/lesson'
    params = {'account': account}

    res = requests.get(url=url, params=params)

    print("response:", res.json())
    return res.json()


def teacher_get_record(account, lesson_id):
    """
        教师根据课程号查看当前课程所有学生课堂表现
        :param lesson_id: 课程号

        :return 返回一个列表，包含学生姓名和上课表现
        格式为:
        (name, sleep_count, sleep_time, talk_count, talk_time
        pry_count, pry_time, absence_count, absence_time,
        total_time, class_period)
    """
    url = root + '/teacher/get/record'
    params = {'lesson_id': lesson_id,
              'account': account}

    res = requests.get(url=url, params=params)

    if res.text == 'LESSON_ID_NOT_EXISTS':
        print("response:", res.text)
        return res.text

    elif res.text == 'LESSON_NOT_BELONG_TEACHER':
        print("response:", res.text)
        return res.text

    print("response:", res.json())
    return res.json()


def student_get_record(account):
    """
        学生查看所有历史课程的表现
        :param account: 学生账号

        :return 返回一个列表，包含课程信息和上课表现
        格式为:
        (datetime, lesson_info, sleep_count, sleep_time, talk_count, talk_time
        pry_count, pry_time, absence_count, absence_time,
        total_time, lesson_period)
        """
    url = root + '/student/get/record'
    params = {'account': account}

    res = requests.get(url=url, params=params)

    print("response:", res.json())
    return res.json()


# 单元测试
if __name__ == '__main__':
    # register_student('student0001', '431322ph', '彭浩')
    # register_teacher('teacher0001', '431322teacher')

    # request_lesson_id('teacher0001', '第一堂课')

    # student_add_lesson('student0001', '00976029614954681310498868609128')

    '''student_post_data('student0001', '06507218065136870324028528085515',
                      sleep_count=3, sleep_time=10,
                      talk_count=2, talk_time=20,
                      pry_count=10, pry_time=3,
                      absence_count=1, absence_time=40,
                      wander_count=20, wander_time=30)'''

    teacher_get_lesson('teacher0001')
    teacher_get_record('06507218065136870324028528085515')
    student_get_record('student0001')

    # login_teacher('teacher0001', '431322teacher')
    # login_teacher('teacher0001', 'xxxx')

    # login_student('student0001', '431322ph')
    # login_student('sfslf', 'lsfks')

