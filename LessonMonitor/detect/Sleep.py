# Author ph
# Company NKCS
# created at 2023/1/1  8:46 PM

def dis(p1, p2):
    return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**0.5


# 判断瞌睡类
class Sleep:
    def __init__(self):
        # 总的帧数
        self.__frame = 0
        # 总的瞌睡次数
        self.__count = 0
        # 总瞌睡时长
        self.__time = 0
        # 当前持续闭眼时长(用于判断是否瞌睡)
        self.__cur = 0

    def update(self, face_landmarks):
        self.__frame += 1
        # 左眼上眼睑
        point1 = face_landmarks.landmark[159]
        # 左眼下眼睑
        point2 = face_landmarks.landmark[145]
        # 右眼上眼睑
        point3 = face_landmarks.landmark[386]
        # 右眼下眼睑
        point4 = face_landmarks.landmark[374]

        dis1 = dis(point1, point2)
        dis2 = dis(point3, point4)

        # 左右眼的上下眼睑高度差通常为0.02-0.03之间
        # 闭眼时高度差通常小于0.008
        if dis1 <= 0.015 and dis2 <= 0.015:
            self.__cur += 1
        else:
            # 连续三帧以上闭眼即视为瞌睡
            if self.__cur > 4:
                self.__count += 1
            # 赋值为0，过滤掉眨眼
            self.__cur = 0

    def check(self):
        if self.__cur > 4:
            self.__time += 1
            return True
        else:
            return False

    # 结束后用于统计睡觉的数据
    def over(self):
        return self.__count, 1.0*self.__time/self.__frame




