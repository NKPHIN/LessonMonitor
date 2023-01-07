# Author ph
# Company NKCS
# created at 2023/1/5  2:42 PM

# 判断缺席类
class Absence:
    def __init__(self):
        self.__frame = 0
        self.__count = 0
        self.__time = 0

        # 保存前一帧的状态，0表示在场，1表示缺席
        self.__flag = 0

    def update(self, face_landmarks):
        self.__frame += 1
        if face_landmarks is None:
            if self.__flag == 0:
                self.__flag = 1
                self.__count += 1
        else:
            self.__flag = 0

    def check(self):
        if self.__flag == 1:
            self.__time += 1
            return True
        else:
            return False

    def over(self):
        return self.__count, 1.0*self.__time/self.__frame
