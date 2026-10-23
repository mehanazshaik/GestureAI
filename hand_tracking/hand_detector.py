import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:

    def __init__(self):

        base_options = python.BaseOptions(
            model_asset_path="hand_tracking/hand_landmarker.task"
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

        self.timestamp_ms = 0

    def detect(self, frame):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp_ms += 33

        result = self.detector.detect_for_video(
            mp_image,
            self.timestamp_ms
        )

        all_landmarks = []

        if result.hand_landmarks:

            height, width, _ = frame.shape

            for hand_landmarks in result.hand_landmarks:

                points = []

                for landmark in hand_landmarks:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    points.append((x, y))

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                for connection in mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS:

                    start = connection.start
                    end = connection.end

                    start_point = points[start]
                    end_point = points[end]

                    cv2.line(
                        frame,
                        start_point,
                        end_point,
                        (255, 0, 0),
                        2
                    )

                all_landmarks.append(points)

        return frame, all_landmarks