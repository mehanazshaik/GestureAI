import math


class GestureRecognizer:

    def calculate_angle(self, point1, point2, point3):

        # point2 is the joint
        vector1 = (
            point1[0] - point2[0],
            point1[1] - point2[1]
        )

        vector2 = (
            point3[0] - point2[0],
            point3[1] - point2[1]
        )

        dot_product = (
            vector1[0] * vector2[0]
            + vector1[1] * vector2[1]
        )

        magnitude1 = math.sqrt(
            vector1[0] ** 2 +
            vector1[1] ** 2
        )

        magnitude2 = math.sqrt(
            vector2[0] ** 2 +
            vector2[1] ** 2
        )

        if magnitude1 == 0 or magnitude2 == 0:
            return 0

        cosine = dot_product / (magnitude1 * magnitude2)

        cosine = max(-1, min(1, cosine))

        angle = math.degrees(
            math.acos(cosine)
        )

        return angle

    def recognize(self, landmarks):

        if not landmarks:
            return "No Hand"

        # --------------------------------
        # INDEX FINGER
        # --------------------------------

        index_angle = self.calculate_angle(
            landmarks[5],
            landmarks[6],
            landmarks[8]
        )

        # --------------------------------
        # MIDDLE FINGER
        # --------------------------------

        middle_angle = self.calculate_angle(
            landmarks[9],
            landmarks[10],
            landmarks[12]
        )

        # --------------------------------
        # RING FINGER
        # --------------------------------

        ring_angle = self.calculate_angle(
            landmarks[13],
            landmarks[14],
            landmarks[16]
        )

        # --------------------------------
        # PINKY
        # --------------------------------

        pinky_angle = self.calculate_angle(
            landmarks[17],
            landmarks[18],
            landmarks[20]
        )

        # --------------------------------
        # FINGER STATUS
        # --------------------------------

        index_extended = index_angle > 150
        middle_extended = middle_angle > 150
        ring_extended = ring_angle > 150
        pinky_extended = pinky_angle > 150

        # --------------------------------
        # ✌️ PEACE
        # --------------------------------

        if (
            index_extended
            and middle_extended
            and not ring_extended
            and not pinky_extended
        ):
            return "Peace"
        
        # 🤟 Make up
        if (
            index_extended
            and not middle_extended
            and not ring_extended
            and pinky_extended
        ):
            return "Make Up"
        # --------------------------------
        # 🖐️ OPEN PALM
        # --------------------------------

        if (
            index_extended
            and middle_extended
            and ring_extended
            and pinky_extended
        ):
            return "Open Palm"

        # --------------------------------
        # FINGERS FOLDED
        # --------------------------------

        fingers_folded = (
            not index_extended
            and not middle_extended
            and not ring_extended
            and not pinky_extended
        )

        if fingers_folded:

            thumb_tip = landmarks[4]
            thumb_base = landmarks[2]
            wrist = landmarks[0]

            thumb_distance = math.sqrt(
                (thumb_tip[0] - wrist[0]) ** 2 +
                (thumb_tip[1] - wrist[1]) ** 2
            )

            thumb_base_distance = math.sqrt(
                (thumb_base[0] - wrist[0]) ** 2 +
                (thumb_base[1] - wrist[1]) ** 2
            )

            # 👍 THUMBS UP
            if thumb_distance > thumb_base_distance * 1.5:
                return "Thumbs Up"

            # ✊ FIST
            return "Fist"

        return "Unknown"