import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QApplication, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QMessageBox, QAbstractItemView
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from client import teacher_get_lesson, request_lesson_id, teacher_get_record


class ComboxDemo(QWidget):
    def __init__(self, account):
        super().__init__()
        # 设置标题
        self.init = True
        self.setWindowTitle('教师系统')
        # 设置初始界面大小
        self.resize(1460, 650)
        # 这几个变量是用来存储用户选择的数据，进行了一个初始化，可以用这个进行传递选择的课程或者课程号啥的
        self.course_content = '请选择课程'
        self.time_content = '请选择时间'
        self.times_content = '请选择上课时段'
        self.course_number = '请输入查询课程号'

        self.account = account

        # 这个位置我预留了三个筛选条件，课程，时间，和时间段，还有一个搜索课程号的搜索框之后再看情况选择删减或者更改吧
        self.course = QComboBox(self)
        self.course.move(10, 15)
        self.course.addItems(['请选择课程', '第一节课', '第二节课', '第三节课'])
        self.course.currentIndexChanged[str].connect(self.print_value)

        self.time = QComboBox(self)
        self.time.move(150, 15)
        self.time.addItems(['请选择时间', '周一', '周二', '周三', '周四', '周五', '周六'])
        self.time.currentIndexChanged[str].connect(self.print_value)  # 条目发生改变，发射信号，传递条目内容

        self.times = QComboBox(self)
        self.times.move(290, 15)
        self.times.addItems(['请选择上课时段', '早上', '下午', '晚自习'])
        self.times.currentIndexChanged[str].connect(self.print_value)  # 条目发生改变，发射信号，传递条目内容

        self.classTime = QLineEdit(self)
        self.classTime.setPlaceholderText('上课时长(min)')
        self.classTime.move(470, 19)

        self.searchLab = QLineEdit(self)
        self.searchLab.setPlaceholderText('请输入查询课程号')

        self.bt1 = QPushButton('确定', self)
        self.bt1.clicked.connect(self.showMessage)
        self.course_number = self.searchLab.text()
        self.searchLab.move(800, 19)
        self.bt1.move(935, 15)

        self.bt2 = QPushButton('新建课程', self)
        self.bt2.clicked.connect(self.newcourse)
        self.bt2.move(605, 15)

        self.bt2 = QPushButton('查看历史授课', self)
        self.bt2.clicked.connect(self.history)
        self.bt2.move(1200, 15)

        self.bt3 = QPushButton('退出登录', self)
        self.bt3.clicked.connect(self.return_login)
        self.bt3.move(1325, 15)

        self.table = QTableWidget(100, 11, parent=self)
        self.table.resize(1395, 600)
        self.table.move(20, 50)

        """
                (name, sleep_count, sleep_time, talk_count, talk_time
                pry_count, pry_time, absence_count, absence_time,
                wander_count, wander_time)
        """
        List = ['姓名', '瞌睡次数', '瞌睡时间/min', '说话次数',
                '说话时间/min', '东张西望次数', '东张西望时间/min',
                '缺席次数', '总缺席时间/min', '录制时长/min', '课堂时长/min']
        self.table.setHorizontalHeaderLabels(List)

        self.course_lens = 3  # 数据总数
        self.showMessage()

    def print_value(self, i):
        print(i)
        if i == '请选择课程' or i == '第一节课' or i == '第二节课' or i == '第三节课':
            self.course_content = i
            print(self.course_content + '!')
        elif i == '请选择时间' or i == '周一' or i == '周二' or i == '周三' or i == '周四' or i == '周五' or i == '周六':
            self.time_content = i
        else:
            self.times_content = i

    def showMessage(self):
        if self.init:
            self.init = False
            return
        if hasattr(self, 'table_history'):
            self.table_history.hide()
        lesson_id = self.searchLab.text()

        if lesson_id == '':
            QMessageBox.warning(self, 'error', '课程号不能为空',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return

        param = teacher_get_record(self.account, lesson_id)

        if param == 'LESSON_ID_NOT_EXISTS' or param == 'LESSON_NOT_BELONG_TEACHER':
            QMessageBox.warning(self, 'error', '该课程号不存在或无权限访问',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return

        self.table.clearContents()
        for i in range(0, 11):
            self.table.setColumnWidth(i, 126)

        for i in range(0, len(param)):
            time_flag = False

            record_time = param[i][9]
            total_time = param[i][10]

            if 1.0 * record_time / total_time < 0.8:
                time_flag = True

            for j in range(0, 11):
                item = QTableWidgetItem()
                item.setText(str(param[i][j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.table.setItem(i, j, item)
                # 提前结束录制标红
                if time_flag:
                    self.table.item(i, j).setBackground(QBrush(QColor(255, 0, 0)))

                # 各种违规动作超过总时长的10%即标黄
                elif 0 < j < 10 and j % 2 == 0 and 1.0 * param[i][j] / record_time > 0.1:
                    self.table.item(i, j).setBackground(QBrush(QColor(255, 255, 0)))

    # 新建课程跳转
    def newcourse(self):
        period = self.classTime.text()
        if period == '':
            QMessageBox.warning(self, 'error', '上课时长不能为空',
                                QMessageBox.Yes, QMessageBox.Yes)
            return
        if not period.isdigit():
            QMessageBox.warning(self, 'error', '上课时长格式错误',
                                QMessageBox.Yes, QMessageBox.Yes)
            return

        self.info = ''
        if self.course_content != '请选择课程':
            self.info += self.course_content + ' '
        if self.time_content != '请选择时间':
            self.info += self.time_content + ' '
        if self.times_content != '请选择上课时段':
            self.info += self.times_content

        lesson_id = request_lesson_id(self.account, period, self.info)
        QMessageBox.information(self, '创建成功', '课程号为:\n' + lesson_id + '\n\n请复制保存',
                                QMessageBox.Yes, QMessageBox.Yes)

    def return_login(self):
        import teacher_login
        self.table = QtWidgets.QWidget()
        self.login_ui = teacher_login.Ui_teacher_login()
        self.login_ui.setupUi(self.table)
        self.table.show()

        self.close()
        self.destroy()

    def history(self):
        param = teacher_get_lesson(self.account)

        self.table_history = QTableWidget(len(param), 4, parent=self)
        self.table_history.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_history.resize(1395, 600)
        self.table_history.move(20, 50)
        List = ['课程号', '时间', '时长', '备注信息']
        self.table_history.setHorizontalHeaderLabels(List)
        self.table_history.setColumnWidth(0, 340)
        self.table_history.setColumnWidth(1, 340)
        self.table_history.setColumnWidth(2, 340)
        self.table_history.setColumnWidth(3, 375)

        for i in range(0, len(param)):
            for j in range(0, 4):
                item = QTableWidgetItem()
                item.setText(str(param[i][j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.table_history.setItem(i, j, item)
        self.table_history.setWindowTitle('课程记录')
        self.table_history.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    comboxDemo = ComboxDemo('teacher0001')
    comboxDemo.show()
    sys.exit(app.exec_())
