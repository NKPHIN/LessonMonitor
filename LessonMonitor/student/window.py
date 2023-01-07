# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
import time

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QDesktopWidget
from client import student_add_lesson, student_post_data, student_get_record
from detect.detect import detect, CountSleep, CountTalk, CountAbsence, CountPry


class Ui_window(object):
    def __init__(self, account):
        self.account = account
        self.lesson_id = ''

        # 定义定时器，用于控制显示视频的帧率
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.setTimerType(Qt.PreciseTimer)
        self.cap = cv2.VideoCapture()
        # 记录起始时间
        self.start = 0.0
        self.end = 0.0

    def setupUi(self, window):
        self.copy = window
        window.setObjectName("window")
        window.setFixedSize(860, 466)
        self.camera = QtWidgets.QLabel(window)
        self.camera.setGeometry(QtCore.QRect(200, 30, 641, 411))
        self.camera.setText("")
        self.camera.setObjectName("camera")
        self.showBackground()
        self.join = QtWidgets.QPushButton(window)
        self.join.setGeometry(QtCore.QRect(40, 80, 100, 32))
        self.join.setObjectName("join")
        self.close = QtWidgets.QPushButton(window)
        self.close.setGeometry(QtCore.QRect(40, 130, 100, 32))
        self.close.setObjectName("close")
        self.close.setEnabled(False)
        self.label = QtWidgets.QLabel(window)
        self.label.setGeometry(QtCore.QRect(30, 30, 145, 16))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.record = QtWidgets.QPushButton(window)
        self.record.setGeometry(QtCore.QRect(40, 180, 100, 32))
        self.record.setObjectName("record")

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

        self.__slot__()

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Form"))
        self.join.setText(_translate("window", "进入课堂"))
        self.close.setText(_translate("window", "结束课程"))
        self.label.setText(_translate("window", "LessonMonitor"))
        self.record.setText(_translate("window", "查看记录"))

    def __slot__(self):
        self.join.clicked.connect(self.joinLesson)
        self.close.clicked.connect(self.closeLesson)
        self.record.clicked.connect(self.getRecord)
        self.timer_camera.timeout.connect(self.show_camera)

    def joinLesson(self):
        lesson_id, ok = QInputDialog.getText(self.copy, "请输入课程号", "如果你还不知道课程号，请联系你的任课老师获取",
                                             QLineEdit.Normal, "32位数字串")
        if ok:
            self.lesson_id = lesson_id
            response = student_add_lesson(self.account, lesson_id)

            if response == 'LESSON_ID_NOT_EXISTS':
                QMessageBox.warning(self.copy, "Error", "该课程号不存在！",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            elif response == 'JOIN_LESSON_REPEAT':
                QMessageBox.warning(self.copy, "Error", "你已加入该课程，请勿重复加入！",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            elif response == 'STUDENT_JOIN_LESSON':
                self.join.setEnabled(False)
                self.close.setEnabled(True)
                self.startTimer()

    def startTimer(self):
        flag = self.cap.open(0)
        if not flag:
            QMessageBox.warning(self.copy, "Error", "请检查相机是否与电脑连接正常",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            # 定时器开始计时30ms，每过30ms从摄像头中取一帧显示
            self.start = time.time()
            self.timer_camera.start(30)

    def show_camera(self):
        flag, self.image = self.cap.read()

        self.image = detect(self.image)

        show = cv2.resize(self.image, (641, 400))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # 把读取到的视频数据变成QImage形式
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 show.shape[1]*3, QtGui.QImage.Format_RGB888)
        # 往显示视频的Label里 显示QImage
        pixmap = QPixmap(showImage)
        self.camera.setPixmap(pixmap)

    def closeLesson(self):
        self.close.setEnabled(False)
        self.join.setEnabled(True)

        # 关闭定时器
        self.timer_camera.stop()
        self.end = time.time()
        # 释放视频流
        self.cap.release()
        self.camera.clear()
        self.showBackground()

        interval = self.end - self.start

        sleep_count, sleep_time = CountSleep()
        sleep_time *= interval
        print('总瞌睡次数:', sleep_count)
        print('总瞌睡时间:', sleep_time, 's')

        talk_count, talk_time = CountTalk()
        talk_time *= interval
        print('总讲话次数:', talk_count)
        print('总讲话时间:', talk_time, 's')

        absence_count, absence_time = CountAbsence()
        absence_time *= interval
        print('总缺席次数:', absence_count)
        print('总缺席时间:', absence_time, 's')

        pry_count, pry_time = CountPry()
        pry_time *= interval
        print('东张西望次数:', pry_count)
        print('东张西望时间:', pry_time, 's')

        print('总时间:', interval, 's')

        sleep_time = round(sleep_time/60, 2)
        talk_time = round(talk_time/60, 2)
        absence_time = round(absence_time/60, 2)
        pry_time = round(pry_time/60, 2)
        interval = round(interval/60, 2)

        student_post_data(self.account, self.lesson_id, sleep_count=sleep_count, sleep_time=sleep_time,
                          talk_count=talk_count, talk_time=talk_time, pry_count=pry_count, pry_time=pry_time,
                          absence_count=absence_count, absence_time=absence_time, total_time=interval)

    def showBackground(self):
        image = QPixmap('./background.png')
        self.camera.setScaledContents(True)
        self.camera.setPixmap(image)

    def getRecord(self):
        # type(record) = 'list'
        self.table = QtWidgets.QWidget()

        record = student_get_record(self.account)

        table = QTableWidget(len(record), 12, parent=self.table)
        table.resize(1200, min(25*len(record)+30, 750))
        table.setHorizontalHeaderLabels(['课程时间', '课程信息', '瞌睡次数', '瞌睡时间',
                                         '讲话次数', '讲话时长', '眼睛离屏次数', '眼睛离屏时长',
                                         '离开课堂次数', '离开课堂时长', '录制时间', '课堂时长'])
        table.setColumnWidth(0, 210)
        for i in range(1, 12):
            table.setColumnWidth(i, 90)
        for i in range(len(record)):
            table.setRowHeight(i, 25)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        r = 0
        for row in record:
            c = 0
            for text in row:
                item = QTableWidgetItem()
                item.setText(str(text))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table.setItem(r, c, item)
                c = c + 1
            r = r + 1

        self.table.setWindowTitle('课程记录')
        self.table.resize(1200, 750)

        screen = QDesktopWidget().screenGeometry()
        size = self.table.geometry()
        self.table.move(int((screen.width() - size.width()) / 2),
                        int((screen.height() - size.height()) / 2))
        self.table.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    ui = Ui_window('nkphin')
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
