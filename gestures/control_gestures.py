import math


class ControlGestureDetector:

    def __init__(self):
        pass

    # =========================================================
    # CALCULATE ANGLE
    # =========================================================

    def calculate_angle(self, a, b, c):

        ba_x = a[0] - b[0]
        ba_y = a[1] - b[1]

        bc_x = c[0] - b[0]
        bc_y = c[1] - b[1]

        dot_product = (
            ba_x * bc_x
            + ba_y * bc_y
        )

        magnitude_ba = math.sqrt(
            ba_x ** 2 + ba_y ** 2
        )

        magnitude_bc = math.sqrt(
            bc_x ** 2 + bc_y ** 2
        )

        if magnitude_ba == 0 or magnitude_bc == 0:
            return 0

        cosine_angle = (
            dot_product
            / (magnitude_ba * magnitude_bc)
        )

        cosine_angle = max(
            -1.0,
            min(1.0, cosine_angle)
        )

        return math.degrees(
            math.acos(cosine_angle)
        )

    # =========================================================
    # GET FINGER ANGLES
    # =========================================================

    def get_finger_angles(self, hand):

        index_angle = self.calculate_angle(
            hand[5],
            hand[6],
            hand[8]
        )

        middle_angle = self.calculate_angle(
            hand[9],
            hand[10],
            hand[12]
        )

        ring_angle = self.calculate_angle(
            hand[13],
            hand[14],
            hand[16]
        )

        pinky_angle = self.calculate_angle(
            hand[17],
            hand[18],
            hand[20]
        )

        return (
            index_angle,
            middle_angle,
            ring_angle,
            pinky_angle
        )

    # =========================================================
    # SCREENSHOT GESTURE ☝️
    # =========================================================

    def is_index_pointing(self, hand):

        (
            index_angle,
            middle_angle,
            ring_angle,
            pinky_angle
        ) = self.get_finger_angles(hand)

        # Index must be straight
        index_extended = (
            index_angle > 155
        )

        # Other fingers must be folded
        middle_folded = (
            middle_angle < 135
        )

        ring_folded = (
            ring_angle < 135
        )

        pinky_folded = (
            pinky_angle < 135
        )

        # Extra safety check
        index_distance = math.dist(
            hand[8],
            hand[0]
        )

        index_mcp_distance = math.dist(
            hand[5],
            hand[0]
        )

        index_long = (
            index_distance
            >
            index_mcp_distance * 1.45
        )

        return (
            index_extended
            and middle_folded
            and ring_folded
            and pinky_folded
            and index_long
        )


    # =========================================================
    # DETECT CONTROL GESTURE
    # =========================================================

    def detect(self, hand):

        if self.is_index_pointing(hand):
            return "SCREENSHOT"

        return None