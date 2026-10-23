import cv2
import math
import numpy as np
from filter_engine.particle_engine import ParticleEngine


class FilterRenderer:

    def __init__(self):
        self.particle_engine = ParticleEngine()

    def draw_goggles(self, frame, face_landmarks):

        if not face_landmarks:
            return frame

        face = face_landmarks[0]

        # Eye points
        left_eye = face[33]
        right_eye = face[263]

        # Distance between eyes
        eye_distance = math.sqrt(
            (right_eye[0] - left_eye[0]) ** 2 +
            (right_eye[1] - left_eye[1]) ** 2
        )

        # Lens size
        width = int(eye_distance * 0.35)
        height = int(eye_distance * 0.20)

        # Lens centers
        left_center = (
            int(left_eye[0]),
            int(left_eye[1])
        )

        right_center = (
            int(right_eye[0]),
            int(right_eye[1])
        )

        # Rotation angle
        angle = math.degrees(
            math.atan2(
                right_eye[1] - left_eye[1],
                right_eye[0] - left_eye[0]
            )
        )

        # Left lens
        cv2.ellipse(
            frame,
            left_center,
            (width, height),
            angle,
            0,
            360,
            (0, 0, 0),
            4
        )

        # Right lens
        cv2.ellipse(
            frame,
            right_center,
            (width, height),
            angle,
            0,
            360,
            (0, 0, 0),
            4
        )

        # Bridge
        cv2.line(
            frame,
            (
                left_center[0] + width,
                left_center[1]
            ),
            (
                right_center[0] - width,
                right_center[1]
            ),
            (0, 0, 0),
            3
        )

        return frame


    def draw_dog_filter(self, frame, face_landmarks):

        if not face_landmarks:
            return frame

        face = face_landmarks[0]

        left_eye = face[33]
        right_eye = face[263]
        nose = face[1]
        lower_lip = face[14]

        face_width = max(
            1,
            int(abs(right_eye[0] - left_eye[0]))
        )

        overlay = frame.copy()

        # =====================================
        # 1. FLOPPY DOG EARS
        # =====================================

        ear_axes = (
            max(2, int(face_width * 0.22)),
            max(2, int(face_width * 0.34))
        )

        left_ear_center = (
            int(left_eye[0] - face_width * 0.24),
            int(left_eye[1] - face_width * 0.30)
        )

        right_ear_center = (
            int(right_eye[0] + face_width * 0.24),
            int(right_eye[1] - face_width * 0.30)
        )

        # Outer ears
        cv2.ellipse(
            overlay,
            left_ear_center,
            ear_axes,
            -25,
            0,
            360,
            (65, 90, 145),
            -1,
            cv2.LINE_AA
        )

        cv2.ellipse(
            overlay,
            right_ear_center,
            ear_axes,
            25,
            0,
            360,
            (65, 90, 145),
            -1,
            cv2.LINE_AA
        )

        # Inner ear shading
        inner_axes = (
            max(2, int(face_width * 0.12)),
            max(2, int(face_width * 0.23))
        )

        cv2.ellipse(
            overlay,
            left_ear_center,
            inner_axes,
            -25,
            0,
            360,
            (105, 125, 185),
            -1,
            cv2.LINE_AA
        )

        cv2.ellipse(
            overlay,
            right_ear_center,
            inner_axes,
            25,
            0,
            360,
            (105, 125, 185),
            -1,
            cv2.LINE_AA
        )

        # =====================================
        # 2. SOFT DOG MUZZLE
        # =====================================

        muzzle_y = int(
            nose[1] + face_width * 0.10
        )

        muzzle_axes = (
            max(2, int(face_width * 0.11)),
            max(2, int(face_width * 0.075))
        )

        # Left side of muzzle
        cv2.ellipse(
            overlay,
            (
                int(nose[0] - face_width * 0.085),
                muzzle_y
            ),
            muzzle_axes,
            0,
            0,
            360,
            (175, 190, 220),
            -1,
            cv2.LINE_AA
        )

        # Right side of muzzle
        cv2.ellipse(
            overlay,
            (
                int(nose[0] + face_width * 0.085),
                muzzle_y
            ),
            muzzle_axes,
            0,
            0,
            360,
            (175, 190, 220),
            -1,
            cv2.LINE_AA
        )

        # =====================================
        # 3. DOG NOSE
        # =====================================

        dog_nose_center = (
            int(nose[0]),
            int(nose[1] + face_width * 0.015)
        )

        nose_axes = (
            max(3, int(face_width * 0.12)),
            max(2, int(face_width * 0.085))
        )

        cv2.ellipse(
            overlay,
            dog_nose_center,
            nose_axes,
            0,
            0,
            360,
            (25, 25, 35),
            -1,
            cv2.LINE_AA
        )

        # Tiny nose shine
        cv2.ellipse(
            overlay,
            (
                dog_nose_center[0] - int(face_width * 0.025),
                dog_nose_center[1] - int(face_width * 0.025)
            ),
            (
                max(1, int(face_width * 0.025)),
                max(1, int(face_width * 0.012))
            ),
            -15,
            0,
            360,
            (190, 190, 200),
            -1,
            cv2.LINE_AA
        )

        # =====================================
        # 4. CUTE PINK TONGUE
        # =====================================

        tongue_center = (
            int(lower_lip[0]),
            int(lower_lip[1] + face_width * 0.09)
        )

        tongue_axes = (
            max(3, int(face_width * 0.085)),
            max(4, int(face_width * 0.15))
        )

        cv2.ellipse(
            overlay,
            tongue_center,
            tongue_axes,
            0,
            0,
            360,
            (120, 90, 235),
            -1,
            cv2.LINE_AA
        )

        # Tongue detail
        cv2.line(
            overlay,
            (
                tongue_center[0],
                tongue_center[1] - int(face_width * 0.02)
            ),
            (
                tongue_center[0],
                tongue_center[1] + int(face_width * 0.09)
            ),
            (155, 115, 205),
            max(1, int(face_width * 0.012)),
            cv2.LINE_AA
        )

        # =====================================
        # 5. BLEND THE FILTER
        # =====================================

        frame = cv2.addWeighted(
            overlay,
            0.92,
            frame,
            0.08,
            0
        )

        return frame


    def draw_bow(self, frame, face_landmarks):

        if not face_landmarks:
            return frame

        face = face_landmarks[0]

        # Eye points
        left_eye = face[33]
        right_eye = face[263]

        # Face width
        face_width = abs(
            right_eye[0] - left_eye[0]
        )

        # --------------------------------
        # BOW POSITION
        # --------------------------------

        bow_x = int(
            left_eye[0] - face_width * 0.30
        )

        bow_y = int(
            left_eye[1] - face_width * 0.45
        )

        # Bow size
        bow_width = int(face_width * 0.22)
        bow_height = int(face_width * 0.15)

        # --------------------------------
        # LEFT BOW LOOP
        # --------------------------------

        cv2.ellipse(
            frame,
            (
                bow_x - bow_width // 2,
                bow_y
            ),
            (
                bow_width // 2,
                bow_height
            ),
            -15,
            0,
            360,
            (180, 105, 255),
            -1
        )

        # --------------------------------
        # RIGHT BOW LOOP
        # --------------------------------

        cv2.ellipse(
            frame,
            (
                bow_x + bow_width // 2,
                bow_y
            ),
            (
                bow_width // 2,
                bow_height
            ),
            15,
            0,
            360,
            (180, 105, 255),
            -1
        )

        # --------------------------------
        # CENTER OF BOW
        # --------------------------------

        cv2.circle(
            frame,
            (bow_x, bow_y),
            int(face_width * 0.07),
            (120, 60, 220),
            -1
        )

        return frame


    def draw_cat_filter(self, frame, face_landmarks):

        if not face_landmarks:
            return frame

        face = face_landmarks[0]

        # Face points
        left_eye = face[33]
        right_eye = face[263]
        nose = face[1]

        # Distance between eyes
        face_width = max(
            1,
            abs(right_eye[0] - left_eye[0])
        )

        # =====================================
        # CAT EAR SIZE
        # =====================================

        ear_size = int(
            face_width * 0.35
        )

        # =====================================
        # EAR POSITIONS
        # =====================================

        left_ear_x = int(
            left_eye[0] - face_width * 0.35
        )

        left_ear_y = int(
            left_eye[1] - face_width * 0.75
        )

        right_ear_x = int(
            right_eye[0] + face_width * 0.35
        )

        right_ear_y = int(
            right_eye[1] - face_width * 0.75
        )

        # =====================================
        # PINK CAT EARS 🩷
        # =====================================

        left_ear = np.array(
            [
                (
                    left_ear_x,
                    left_ear_y + ear_size
                ),
                (
                    left_ear_x - ear_size // 2,
                    left_ear_y
                ),
                (
                    left_ear_x + ear_size // 2,
                    left_ear_y
                )
            ],
            dtype=np.int32
        )

        right_ear = np.array(
            [
                (
                    right_ear_x,
                    right_ear_y + ear_size
                ),
                (
                    right_ear_x - ear_size // 2,
                    right_ear_y
                ),
                (
                    right_ear_x + ear_size // 2,
                    right_ear_y
                )
            ],
            dtype=np.int32
        )

        # Outer pink ears
        cv2.fillPoly(
            frame,
            [left_ear],
            (150, 80, 220)
        )

        cv2.fillPoly(
            frame,
            [right_ear],
            (150, 80, 220)
        )

        # =====================================
        # INNER PINK EARS
        # =====================================

        inner_size = int(
            ear_size * 0.58
        )

        left_inner = np.array(
            [
                (
                    left_ear_x,
                    left_ear_y + inner_size
                ),
                (
                    left_ear_x - inner_size // 2,
                    left_ear_y + int(ear_size * 0.15)
                ),
                (
                    left_ear_x + inner_size // 2,
                    left_ear_y + int(ear_size * 0.15)
                )
            ],
            dtype=np.int32
        )

        right_inner = np.array(
            [
                (
                    right_ear_x,
                    right_ear_y + inner_size
                ),
                (
                    right_ear_x - inner_size // 2,
                    right_ear_y + int(ear_size * 0.15)
                ),
                (
                    right_ear_x + inner_size // 2,
                    right_ear_y + int(ear_size * 0.15)
                )
            ],
            dtype=np.int32
        )

        # Lighter pink inner ears
        cv2.fillPoly(
            frame,
            [left_inner],
            (190, 120, 245)
        )

        cv2.fillPoly(
            frame,
            [right_inner],
            (190, 120, 245)
        )

        # =====================================
        # SMALL PINK CAT NOSE 🩷
        # =====================================

        nose_radius = max(
            2,
            int(face_width * 0.035)
        )

        cv2.circle(
            frame,
            nose,
            nose_radius,
            (150, 90, 220),
            -1,
            cv2.LINE_AA
        )

        # Tiny highlight on nose
        cv2.circle(
            frame,
            (
                nose[0] - int(nose_radius * 0.30),
                nose[1] - int(nose_radius * 0.30)
            ),
            max(1, int(nose_radius * 0.25)),
            (235, 190, 255),
            -1,
            cv2.LINE_AA
        )

        # =====================================
        # WHISKERS 🩷
        # =====================================

        # Small gap between nose and whiskers
        gap = int(
            face_width * 0.12
        )

        whisker_length = int(
            face_width * 0.28
        )

        whisker_spacing = int(
            face_width * 0.065
        )

        whisker_color = (150, 90, 220)

        whisker_thickness = max(
            1,
            int(face_width * 0.012)
        )

        # -------------------------------------
        # LEFT CHEEK - 3 WHISKERS
        # -------------------------------------

        start_x_left = nose[0] - gap

        cv2.line(
            frame,
            (
                start_x_left,
                nose[1] - whisker_spacing
            ),
            (
                start_x_left - whisker_length,
                nose[1] - whisker_spacing * 2
            ),
            whisker_color,
            whisker_thickness,
            cv2.LINE_AA
        )

        cv2.line(
            frame,
            (
                start_x_left,
                nose[1]
            ),
            (
                start_x_left - whisker_length,
                nose[1]
            ),
            whisker_color,
            whisker_thickness,
            cv2.LINE_AA
        )

        cv2.line(
            frame,
            (
                start_x_left,
                nose[1] + whisker_spacing
            ),
            (
                start_x_left - whisker_length,
                nose[1] + whisker_spacing * 2
            ),
            whisker_color,
            whisker_thickness,
            cv2.LINE_AA
        )

        # -------------------------------------
        # RIGHT CHEEK - 3 WHISKERS
        # -------------------------------------

        start_x_right = nose[0] + gap

        cv2.line(
            frame,
            (
                start_x_right,
                nose[1] - whisker_spacing
            ),
            (
                start_x_right + whisker_length,
                nose[1] - whisker_spacing * 2
            ),
            whisker_color,
            whisker_thickness,
            cv2.LINE_AA
        )

        cv2.line(
            frame,
            (
                start_x_right,
                nose[1]
            ),
            (
                start_x_right + whisker_length,
                nose[1]
            ),
            whisker_color,
            whisker_thickness,
            cv2.LINE_AA
        )

        cv2.line(
            frame,
            (
                start_x_right,
                nose[1] + whisker_spacing
            ),
            (
                start_x_right + whisker_length,
                nose[1] + whisker_spacing * 2
            ),
            whisker_color,
            whisker_thickness,
            cv2.LINE_AA
        )

        return frame
    
    def draw_heart_filter(self, frame, face_landmarks):

        if not face_landmarks:
            return frame

        face = face_landmarks[0]

        # Face landmarks
        left_eye = face[33]
        right_eye = face[263]

        # Calculate face width
        face_width = abs(
            right_eye[0] - left_eye[0]
        )

        # Forehead position
        center_x = int(
            (left_eye[0] + right_eye[0]) / 2
        )

        forehead_y = int(
            left_eye[1] - face_width * 0.65
        )

        # Create a heart at controlled intervals
        self.particle_engine.create_heart(
            center_x,
            forehead_y
        )

        # Update particle positions and lifetimes
        self.particle_engine.update()

        # Draw every active heart
        for heart in self.particle_engine.hearts:

            # Fade hearts near the end of their lifetime
            alpha = min(
                1.0,
                heart["life"] / 20.0
            )

            alpha = max(0.0, alpha)

            # Draw on a separate overlay
            overlay = frame.copy()

            self.draw_heart(
                overlay,
                int(heart["x"]),
                int(heart["y"]),
                int(heart["size"])
            )

            # Blend the heart into the camera frame
            frame = cv2.addWeighted(
                overlay,
                alpha,
                frame,
                1.0 - alpha,
                0
            )

        return frame


    def draw_heart(self, frame, x, y, size):

        # Two circles at the top
        radius = max(1, int(size * 0.35))

        cv2.circle(
            frame,
            (x - radius, y),
            radius,
            (80, 0, 255),
            -1
        )

        cv2.circle(
            frame,
            (x + radius, y),
            radius,
            (80, 0, 255),
            -1
        )

        # Triangle underneath the circles
        points = [
            (
                x - int(size * 0.7),
                y + int(size * 0.1)
            ),
            (
                x + int(size * 0.7),
                y + int(size * 0.1)
            ),
            (
                x,
                y + int(size * 0.9)
            )
        ]

        cv2.fillPoly(
            frame,
            [np.array(points, dtype=np.int32)],
            (80, 0, 255)
        )

    def draw_makeup_filter(self, frame, face_landmarks):

        if not face_landmarks:
            return frame

        face = face_landmarks[0]

        left_eye = face[33]
        right_eye = face[263]

        face_width = max(
            1,
            int(abs(right_eye[0] - left_eye[0]))
        )

        # =====================================
        # 1. NATURAL SOFT BLUSH
        # =====================================

        blush_mask = np.zeros(
            frame.shape[:2],
            dtype=np.uint8
        )

        # Position cheeks below the eyes
        left_cheek = (
            int(left_eye[0] + face_width * 0.15),
            int(left_eye[1] + face_width * 0.42)
        )

        right_cheek = (
            int(right_eye[0] - face_width * 0.15),
            int(right_eye[1] + face_width * 0.42)
        )

        # Soft oval shapes instead of solid circles
        cheek_axes = (
            max(2, int(face_width * 0.17)),
            max(2, int(face_width * 0.10))
        )

        cv2.ellipse(
            blush_mask,
            left_cheek,
            cheek_axes,
            0,
            0,
            360,
            255,
            -1,
            cv2.LINE_AA
        )

        cv2.ellipse(
            blush_mask,
            right_cheek,
            cheek_axes,
            0,
            0,
            360,
            255,
            -1,
            cv2.LINE_AA
        )

        # Blur only the mask, not the camera image
        cv2.GaussianBlur(
            blush_mask,
            (0, 0),
            sigmaX=max(2, face_width * 0.07),
            dst=blush_mask
        )

        # Soft pink blush
        blush_color = np.zeros_like(frame)
        blush_color[:] = (125, 115, 225)

        blush_alpha = (
            blush_mask.astype(np.float32) / 255.0
        ) * 0.18

        blush_alpha = blush_alpha[:, :, np.newaxis]

        frame = (
            frame.astype(np.float32) *
            (1.0 - blush_alpha) +
            blush_color.astype(np.float32) *
            blush_alpha
        ).astype(np.uint8)

        # =====================================
        # 2. NATURAL PINK LIP TINT
        # =====================================

        # Outer lip landmarks
        lip_indices = [
            61, 146, 91, 181, 84, 17,
            314, 405, 321, 375, 291,
            409, 270, 269, 267, 0,
            37, 39, 40, 185
        ]

        lip_points = np.array(
            [face[i] for i in lip_indices],
            dtype=np.int32
        )

        # Create lipstick mask
        lip_mask = np.zeros(
            frame.shape[:2],
            dtype=np.uint8
        )

        cv2.fillPoly(
            lip_mask,
            [lip_points],
            255,
            lineType=cv2.LINE_AA
        )

        # Smooth the lip boundary
        lip_mask = cv2.GaussianBlur(
            lip_mask,
            (5, 5),
            0
        )

        # Natural rosy pink
        lipstick_color = np.zeros_like(frame)

        lipstick_color[:] = (
            105,
            75,
            165
        )

        # Much lighter transparency
        lip_alpha = (
            lip_mask.astype(np.float32) / 255.0
        ) * 0.16

        lip_alpha = lip_alpha[:, :, np.newaxis]

        frame = (
            frame.astype(np.float32) *
            (1.0 - lip_alpha) +
            lipstick_color.astype(np.float32) *
            lip_alpha
        ).astype(np.uint8)
        # =====================================
        # 3. SUBTLE NOSE HIGHLIGHT
        # =====================================

        nose = face[1]

        highlight_mask = np.zeros(
            frame.shape[:2],
            dtype=np.uint8
        )

        highlight_center = (
            int(nose[0]),
            int(nose[1] - face_width * 0.025)
        )

        highlight_axes = (
            max(1, int(face_width * 0.025)),
            max(2, int(face_width * 0.055))
        )

        cv2.ellipse(
            highlight_mask,
            highlight_center,
            highlight_axes,
            0,
            0,
            360,
            255,
            -1,
            cv2.LINE_AA
        )

        cv2.GaussianBlur(
            highlight_mask,
            (0, 0),
            sigmaX=max(1, face_width * 0.015),
            dst=highlight_mask
        )

        highlight_color = np.zeros_like(frame)
        highlight_color[:] = (205, 205, 235)

        highlight_alpha = (
            highlight_mask.astype(np.float32) / 255.0
        ) * 0.10

        highlight_alpha = highlight_alpha[:, :, np.newaxis]

        frame = (
            frame.astype(np.float32) *
            (1.0 - highlight_alpha) +
            highlight_color.astype(np.float32) *
            highlight_alpha
        ).astype(np.uint8)
        # =====================================
        # 4. WHITE 6-PETAL FLOWER 🌼
        # =====================================

        flower_x = int(
            left_eye[0] - face_width * 0.30
        )

        flower_y = int(
            left_eye[1] - face_width * 0.45
        )

        # Slightly bigger flower
        flower_size = max(
            10,
            int(face_width * 0.17)
        )

        flower_overlay = frame.copy()

        # -------------------------------------
        # White elongated flower petals 🌼
        # -------------------------------------

        petal_color = (245, 245, 245)

        petal_distance = int(
            flower_size * 0.62
        )

        petal_width = max(
            5,
            int(flower_size * 0.42)
        )

        petal_height = max(
            7,
            int(flower_size * 0.62)
        )

        # Six petals with different rotations
        petals = [
            # Top
            (
                flower_x,
                flower_y - petal_distance,
                0
            ),

            # Top-right
            (
                flower_x + int(petal_distance * 0.87),
                flower_y - int(petal_distance * 0.50),
                60
            ),

            # Bottom-right
            (
                flower_x + int(petal_distance * 0.87),
                flower_y + int(petal_distance * 0.50),
                -60
            ),

            # Bottom
            (
                flower_x,
                flower_y + petal_distance,
                0
            ),

            # Bottom-left
            (
                flower_x - int(petal_distance * 0.87),
                flower_y + int(petal_distance * 0.50),
                60
            ),

            # Top-left
            (
                flower_x - int(petal_distance * 0.87),
                flower_y - int(petal_distance * 0.50),
                -60
            )
        ]

        for petal_x, petal_y, angle in petals:

            cv2.ellipse(
                flower_overlay,
                (
                    petal_x,
                    petal_y
                ),
                (
                    petal_width,
                    petal_height
                ),
                angle,
                0,
                360,
                petal_color,
                -1,
                cv2.LINE_AA
            )

        # -------------------------------------
        # Yellow center 🌼
        # -------------------------------------

        center_radius = max(
            5,
            int(flower_size * 0.32)
        )

        cv2.circle(
            flower_overlay,
            (
                flower_x,
                flower_y
            ),
            center_radius,
            (0, 190, 255),
            -1,
            cv2.LINE_AA
        )

        # Small yellow center highlight
        cv2.circle(
            flower_overlay,
            (
                flower_x - int(center_radius * 0.25),
                flower_y - int(center_radius * 0.25)
            ),
            max(
                1,
                int(center_radius * 0.25)
            ),
            (40, 220, 255),
            -1,
            cv2.LINE_AA
        )

        # -------------------------------------
        # Soft blending
        # -------------------------------------

        frame = cv2.addWeighted(
            flower_overlay,
            0.92,
            frame,
            0.08,
            0
        )

        return frame