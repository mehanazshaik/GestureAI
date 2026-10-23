import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceDetector:

    def __init__(self):

        base_options = python.BaseOptions(
            model_asset_path="face_tracking/face_landmarker.task"
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_faces=2,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = vision.FaceLandmarker.create_from_options(
            options
        )

        self.timestamp_ms = 0

    def detect(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp_ms += 33

        result = self.detector.detect_for_video(
            mp_image,
            self.timestamp_ms
        )

        face_landmarks = []

        if result.face_landmarks:

            height, width, _ = frame.shape

            for face in result.face_landmarks:

                points = []

                for landmark in face:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    points.append((x, y))

                

                face_landmarks.append(points)

        return frame, face_landmarks