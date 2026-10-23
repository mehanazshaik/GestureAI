import cv2
import time

from gestures.control_gestures import ControlGestureDetector
from control_mode.controller import GestureController
from hand_tracking.gesture_recognizer import GestureRecognizer
from camera.camera_manager import CameraManager
from hand_tracking.hand_detector import HandDetector
from ml.feature_extractor import FeatureExtractor
from face_tracking.face_detector import FaceDetector
from filter_engine.filter_renderer import FilterRenderer
from gestures.heart_gesture import HeartGesture


# =========================================================
# FIND FACE NEAREST TO ONE HAND
# =========================================================

def find_nearest_face(hand_landmarks, face_landmarks):

    if not face_landmarks:
        return None

    hand_x, hand_y = hand_landmarks[0]

    nearest_face = None
    smallest_distance = float("inf")

    for face in face_landmarks:

        face_x, face_y = face[1]

        distance = (
            (hand_x - face_x) ** 2
            + (hand_y - face_y) ** 2
        )

        if distance < smallest_distance:
            smallest_distance = distance
            nearest_face = face

    return nearest_face


# =========================================================
# FIND FACE NEAREST TO TWO-HAND HEART
# =========================================================

def find_heart_face(hand_landmarks, face_landmarks):

    if len(hand_landmarks) < 2:
        return None

    if not face_landmarks:
        return None

    hand1_x, hand1_y = hand_landmarks[0][0]
    hand2_x, hand2_y = hand_landmarks[1][0]

    heart_x = (hand1_x + hand2_x) // 2
    heart_y = (hand1_y + hand2_y) // 2

    nearest_face = None
    smallest_distance = float("inf")

    for face in face_landmarks:

        face_x, face_y = face[1]

        distance = (
            (heart_x - face_x) ** 2
            + (heart_y - face_y) ** 2
        )

        if distance < smallest_distance:
            smallest_distance = distance
            nearest_face = face

    return nearest_face


# =========================================================
# DRAW USER INTERFACE
# =========================================================

def draw_ui(frame, detected_gesture, screenshot_message):

    height, width = frame.shape[:2]

    # -----------------------------------------------------
    # TOP BAR
    # -----------------------------------------------------

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (width, 80),
        (0, 0, 0),
        -1
    )

    frame = cv2.addWeighted(
        overlay,
        0.55,
        frame,
        0.45,
        0
    )

    # -----------------------------------------------------
    # APP TITLE
    # -----------------------------------------------------

    cv2.putText(
        frame,
        "GestureAR",
        (25, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Real-Time Gesture Controlled AR",
        (25, 62),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (220, 220, 220),
        1
    )

    # -----------------------------------------------------
    # LIVE STATUS
    # -----------------------------------------------------

    cv2.circle(
        frame,
        (width - 90, 28),
        7,
        (0, 255, 0),
        -1
    )

    cv2.putText(
        frame,
        "LIVE",
        (width - 72, 34),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # -----------------------------------------------------
    # DETECTED GESTURE
    # -----------------------------------------------------

    if detected_gesture:

        text = "Detected: " + detected_gesture

        cv2.rectangle(
            frame,
            (20, 95),
            (310, 140),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            text,
            (35, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

    # -----------------------------------------------------
    # SCREENSHOT MESSAGE
    # -----------------------------------------------------

    if screenshot_message:

        message = "Screenshot Captured!"

        text_size = cv2.getTextSize(
            message,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            2
        )[0]

        box_width = text_size[0] + 40

        x1 = max(
            10,
            (width - box_width) // 2
        )

        x2 = min(
            width - 10,
            x1 + box_width
        )

        cv2.rectangle(
            frame,
            (x1, 155),
            (x2, 200),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            message,
            (x1 + 20, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

    # -----------------------------------------------------
    # BOTTOM GESTURE GUIDE
    # -----------------------------------------------------

    guide_height = 92

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, height - guide_height),
        (width, height),
        (0, 0, 0),
        -1
    )

    frame = cv2.addWeighted(
        overlay,
        0.60,
        frame,
        0.40,
        0
    )

    cv2.putText(
        frame,
        "PEACE: Goggles   THUMBS UP: Dog   FIST: Cat   OPEN PALM: Bow",
        (20, height - 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.42,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        "MAKE UP: Makeup   HEART: Hearts   INDEX: Screenshot   Q: Quit",
        (20, height - 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.42,
        (255, 255, 255),
        1
    )

    return frame


# =========================================================
# MAIN
# =========================================================

def main():

    # -----------------------------------------------------
    # INITIALIZE COMPONENTS
    # -----------------------------------------------------

    camera = CameraManager()

    feature_extractor = FeatureExtractor()

    hand_detector = HandDetector()

    gesture_recognizer = GestureRecognizer()

    face_detector = FaceDetector()

    filter_renderer = FilterRenderer()

    heart_gesture = HeartGesture()

    # Screenshot gesture detector
    control_detector = ControlGestureDetector()

    # Used only for saving screenshots
    gesture_controller = GestureController()

    # -----------------------------------------------------
    # SCREENSHOT STATE
    # -----------------------------------------------------

    previous_screenshot_detected = False
    screenshot_requested = False

    # -----------------------------------------------------
    # UI STATE
    # -----------------------------------------------------

    detected_gesture = ""

    screenshot_message = False
    screenshot_message_time = 0

    # -----------------------------------------------------
    # CHECK CAMERA
    # -----------------------------------------------------

    if not camera.camera.isOpened():

        print("Error: Camera could not be opened.")
        return

    # -----------------------------------------------------
    # CLEAN TERMINAL STARTUP
    # -----------------------------------------------------

    print()
    print("========================================")
    print("           GestureAR Started")
    print("========================================")
    print("Camera Ready")
    print()
    print("Available Gestures:")
    print("Peace      -> Goggles")
    print("Thumbs Up  -> Dog")
    print("Fist       -> Cat")
    print("Open Palm  -> Bow")
    print("Make Up    -> Makeup")
    print("Heart      -> Floating Hearts")
    print("Index      -> Screenshot")
    print()
    print("Press Q to Quit")
    print("========================================")
    print()

    # =====================================================
    # CAMERA LOOP
    # =====================================================

    while True:

        heart_detected = False
        screenshot_detected = False

        detected_gesture = ""

        # -------------------------------------------------
        # READ CAMERA
        # -------------------------------------------------

        success, frame = camera.camera.read()

        if not success:

            print("Could not read camera frame.")
            break

        # -------------------------------------------------
        # HAND DETECTION
        # -------------------------------------------------

        frame, landmarks = hand_detector.detect(
            frame
        )

        # -------------------------------------------------
        # FACE DETECTION
        # -------------------------------------------------

        frame, face_landmarks = face_detector.detect(
            frame
        )

        # =================================================
        # HAND PROCESSING
        # =================================================

        if landmarks:

            # Keep existing feature extraction
            features = feature_extractor.extract(
                landmarks[0]
            )

            # =================================================
            # 1. HEART DETECTION FIRST
            # =================================================

            if len(landmarks) >= 2:

                heart_detected = heart_gesture.detect(
                    landmarks
                )

            # =================================================
            # 2. HEART FILTER
            # =================================================

            if heart_detected:

                detected_gesture = "Heart"

                heart_face = find_heart_face(
                    landmarks,
                    face_landmarks
                )

                if heart_face is not None:

                    frame = (
                        filter_renderer
                        .draw_heart_filter(
                            frame,
                            [heart_face]
                        )
                    )

            # =================================================
            # 3. NORMAL AR GESTURES
            # =================================================

            else:

                for hand in landmarks:

                    person_gesture = (
                        gesture_recognizer.recognize(
                            hand
                        )
                    )

                    # -----------------------------------------
                    # MATCH HAND TO NEAREST FACE
                    # -----------------------------------------

                    matched_face = find_nearest_face(
                        hand,
                        face_landmarks
                    )

                    if matched_face is None:
                        continue

                    person_face = [
                        matched_face
                    ]

                    # =========================================
                    # PEACE -> GOGGLES
                    # =========================================

                    if person_gesture == "Peace":

                        detected_gesture = "Peace"

                        frame = (
                            filter_renderer
                            .draw_goggles(
                                frame,
                                person_face
                            )
                        )

                    # =========================================
                    # THUMBS UP -> DOG
                    # =========================================

                    elif person_gesture == "Thumbs Up":

                        detected_gesture = "Thumbs Up"

                        frame = (
                            filter_renderer
                            .draw_dog_filter(
                                frame,
                                person_face
                            )
                        )

                    # =========================================
                    # OPEN PALM -> BOW
                    # =========================================

                    elif person_gesture == "Open Palm":

                        detected_gesture = "Open Palm"

                        frame = (
                            filter_renderer
                            .draw_bow(
                                frame,
                                person_face
                            )
                        )

                    # =========================================
                    # FIST -> CAT
                    # =========================================

                    elif person_gesture == "Fist":

                        detected_gesture = "Fist"

                        frame = (
                            filter_renderer
                            .draw_cat_filter(
                                frame,
                                person_face
                            )
                        )

                    # =========================================
                    # MAKE UP -> MAKEUP
                    # =========================================

                    elif person_gesture == "Make Up":

                        detected_gesture = "Make Up"

                        frame = (
                            filter_renderer
                            .draw_makeup_filter(
                                frame,
                                person_face
                            )
                        )

            # =================================================
            # 4. SCREENSHOT DETECTION
            # =================================================

            for hand in landmarks:

                control_action = (
                    control_detector.detect(
                        hand
                    )
                )

                if control_action == "SCREENSHOT":

                    screenshot_detected = True
                    break

        # =================================================
        # 5. SCREENSHOT EDGE DETECTION
        # =================================================

        screenshot_triggered = (
            screenshot_detected
            and not previous_screenshot_detected
        )

        if screenshot_triggered:

            screenshot_requested = True

        previous_screenshot_detected = (
            screenshot_detected
        )

        # =================================================
        # 6. SAVE SCREENSHOT
        # =================================================
        #
        # Keep this BEFORE draw_ui().
        #
        # This means:
        # - AR filters ARE saved
        # - UI bars/text are NOT saved
        #
        # So the screenshot stays clean.
        # =================================================

        if screenshot_requested:

            gesture_controller.take_screenshot(
                frame
            )

            screenshot_requested = False

            screenshot_message = True
            screenshot_message_time = time.time()

        # -------------------------------------------------
        # HIDE SCREENSHOT MESSAGE AFTER 1.5 SECONDS
        # -------------------------------------------------

        if screenshot_message:

            if (
                time.time()
                - screenshot_message_time
                > 1.5
            ):

                screenshot_message = False

        # =================================================
        # 7. DRAW UI
        # =================================================

        frame = draw_ui(
            frame,
            detected_gesture,
            screenshot_message
        )

        # =================================================
        # 8. SHOW CAMERA
        # =================================================

        cv2.imshow(
            "GestureAR",
            frame
        )

        # =================================================
        # QUIT
        # =================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):

            print()
            print("GestureAR Closed")
            break

    # =====================================================
    # CLEANUP
    # =====================================================

    camera.camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()