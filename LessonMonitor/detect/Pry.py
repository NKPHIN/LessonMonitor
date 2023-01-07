# Author ph
# Company NKCS
# created at 2023/1/5  2:31 PM

def dis(p1, p2):
    return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**0.5


# 判断东张西望类
class Pry:
    def __init__(self):
        self.__frame = 0
        self.__count = 0
        self.__time = 0

        # 0表示视线在屏幕中，1表示东张西望
        self.__flag = 0

    def update(self, face_landmarks):
        """
            十个点位用来描述瞳孔，编号是468-477，编号规则如下：
                    470                     475
            471     468     469     476     473     474
                    472                     477
                  左眼瞳孔                  右眼瞳孔
        """
        self.__frame += 1

        point1 = face_landmarks.landmark[468]      # 左眼瞳孔中心
        point2 = face_landmarks.landmark[473]      # 右眼瞳孔中心

        point3 = face_landmarks.landmark[33]       # 左眼 左眼角
        point4 = face_landmarks.landmark[133]      # 左眼 右眼角
        point5 = face_landmarks.landmark[159]      # 左眼 上眼睑
        point6 = face_landmarks.landmark[145]      # 左眼 下眼睑

        point7 = face_landmarks.landmark[362]      # 右眼 左眼角
        point8 = face_landmarks.landmark[263]      # 右眼 右眼角
        point9 = face_landmarks.landmark[386]      # 右眼 上眼睑
        point10 = face_landmarks.landmark[374]     # 右眼 下眼睑

        dis1 = dis(point1, point3)                 # 左眼: 瞳孔中心到左眼角的距离   通常在0.019-0.022之间
        dis2 = dis(point1, point4)                 # 左眼: 瞳孔中心到右眼角的距离   通常在0.022-0.025之间
        dis3 = dis(point1, point5)                 # 左眼: 瞳孔中心到上眼睑的距离   通常在0.005-0.008之间
        dis4 = dis(point1, point6)                 # 左眼: 瞳孔中心到下眼睑的距离   通常在0.011-0.014之间

        dis5 = dis(point2, point7)                 # 右眼: 瞳孔中心到左眼角的距离   通常在0.025-0.028之间
        dis6 = dis(point2, point8)                 # 右眼: 瞳孔中心到右眼角的距离   通常在0.020-0.023之间
        dis7 = dis(point2, point9)                 # 右眼: 瞳孔中心到上眼睑的距离   通常在0.006-0.009之间
        dis8 = dis(point2, point10)                # 右眼: 瞳孔中心到下眼睑的距离   通常在0.013-0.016之间

        ratio1 = dis1/dis2                         # 左眼 左右比例 通常为0.85-0.93
        # ratio2 = dis3/dis4                         # 左眼 上下比例 通常为0.70-0.75
        ratio3 = dis5/dis6                         # 右眼 左右比例 通常为1.05-1.15
        # ratio4 = dis7/dis8                         # 右眼 上下比例 通常为0.65-0.75

        if ratio1 >= 1.4 or ratio1 <= 0.6:
            self.__flag = 1

        elif ratio3 >= 1.6 or ratio3 <= 0.8:
            self.__flag = 1

        else:
            if self.__flag == 1:
                self.__count += 1
                self.__flag = 0

    def check(self):
        if self.__flag == 1:
            self.__time += 1
            return True
        else:
            return False

    def over(self):
        return self.__count, 1.0*self.__time/self.__frame





