# Author ph
# Company NKCS
# created at 2023/1/2  5:04 PM

import cv2
import mediapipe as mp
from detect.Sleep import Sleep
from detect.Talk import Talk
from detect.Absence import Absence
from detect.Pry import Pry

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
sleep_monitor = Sleep()
talk_monitor = Talk()
absence_monitor = Absence()
pry_monitor = Pry()


def detect(image):
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
                sleep_monitor.update(face_landmarks)
                talk_monitor.update(face_landmarks)
                pry_monitor.update(face_landmarks)
                absence_monitor.update(face_landmarks)
        else:
            absence_monitor.update(None)

        image = cv2.flip(image, 1)
        if sleep_monitor.check():
            text = "Don't sleep on class!"
            cv2.putText(image, text, (300, 100), cv2.FONT_HERSHEY_COMPLEX, 2.0, (240, 5, 5), 5)
        if talk_monitor.check():
            text = "Don't Talk on class!"
            cv2.putText(image, text, (300, 200), cv2.FONT_HERSHEY_COMPLEX, 2.0, (240, 5, 5), 5)
        if pry_monitor.check():
            text = "Don't Pry on class!"
            cv2.putText(image, text, (300, 300), cv2.FONT_HERSHEY_COMPLEX, 2.0, (240, 5, 5), 5)
        if absence_monitor.check():
            text = "Don't leave on class!"
            cv2.putText(image, text, (300, 400), cv2.FONT_HERSHEY_COMPLEX, 2.0, (240, 5, 5), 5)

        return image


# 统计睡觉数据
def CountSleep():
    return sleep_monitor.over()


# 统计讲话数据
def CountTalk():
    return talk_monitor.over()


# 统计缺席数据
def CountAbsence():
    return absence_monitor.over()


# 统计东张西望数据
def CountPry():
    return pry_monitor.over()
