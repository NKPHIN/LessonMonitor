# Author ph
# Company NKCS
# created at 2023/1/2  5:26 PM

# 返回两点间的距离
def dis(p1, p2):
    return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**0.5


# 判断讲话类
class Talk:
    def __init__(self):
        # 总帧数
        self.__frame = 0
        # 总的说话次数
        self.__count = 0
        # 总的说话时长
        self.__time = 0
        # 嘴巴长宽比
        self.ratio = 0.0
        # 当前长宽比连续变化次数(正常闭合状态波动不超过0.03)
        self.change = 0
        # 当前长宽比连续稳定次数
        self.stable = 0

    def update(self, face_landmarks):
        self.__frame += 1

        # 上唇中间
        point1 = face_landmarks.landmark[12]
        # 下唇中间
        point2 = face_landmarks.landmark[15]
        # 左唇角
        point3 = face_landmarks.landmark[62]
        # 右唇角
        point4 = face_landmarks.landmark[292]

        # 上唇中间和下唇中间的距离
        dis1 = dis(point1, point2)
        # 左唇角与右唇角的距离
        dis2 = dis(point3, point4)
        # 长宽比
        cur = dis1 / dis2

        # 过滤抿嘴和 移动造成的比例波动
        if dis1 <= 0.01:
            self.change = 0
            return
        # 过滤咳嗽
        if cur >= 1.0:
            # 哈欠打完后复位会被检测为说话，因此用-3抵消
            self.change = -3
            return

        if self.ratio == 0.0:
            self.ratio = cur
        # 长宽比波动超过0.03则认为是一次变化
        elif abs(self.ratio - cur > 0.03):
            self.stable = 0
            self.change += 1
            self.ratio = cur
        else:
            self.ratio = cur
            self.stable += 1

        if self.stable >= 10:
            if self.change >= 3:
                self.__count += 1
            # 过滤嘴巴单次波动
            self.change = 0

    def check(self):
        # 长宽比连续变化三次以上即认为是说话
        if self.change >= 3:
            self.__time += 1
            return True
        else:
            return False

    # 结束后用于统计讲话的数据
    def over(self):
        return self.__count, 1.0*self.__time/self.__frame
