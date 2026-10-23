import math


class HeartGesture:

    def calculate_distance(self, point1, point2):

        return math.sqrt(
            (point1[0] - point2[0]) ** 2 +
            (point1[1] - point2[1]) ** 2
        )

    def detect(self, hands):

        # We need exactly two detected hands
        if len(hands) < 2:
            return False

        hand1 = hands[0]
        hand2 = hands[1]

        # --------------------------------
        # IMPORTANT POINTS
        # --------------------------------

        # Thumb tips
        thumb1 = hand1[4]
        thumb2 = hand2[4]

        # Index finger tips
        index1 = hand1[8]
        index2 = hand2[8]

        # --------------------------------
        # DISTANCES
        # --------------------------------

        thumb_distance = self.calculate_distance(
            thumb1,
            thumb2
        )

        index_distance = self.calculate_distance(
            index1,
            index2
        )

        # Distance between the two hands
        hand_distance = self.calculate_distance(
            hand1[0],
            hand2[0]
        )

        # --------------------------------
        # NORMALIZE USING HAND SIZE
        # --------------------------------

        hand1_size = self.calculate_distance(
            hand1[0],
            hand1[9]
        )

        hand2_size = self.calculate_distance(
            hand2[0],
            hand2[9]
        )

        average_hand_size = (
            hand1_size + hand2_size
        ) / 2

        if average_hand_size == 0:
            return False

        # --------------------------------
        # HEART CONDITIONS
        # --------------------------------

        thumbs_close = (
            thumb_distance <
            average_hand_size * 1.5
        )

        indexes_close = (
            index_distance <
            average_hand_size * 1.5
        )

        hands_close = (
            hand_distance <
            average_hand_size * 4
        )

        # --------------------------------
        # HEART DETECTED
        # --------------------------------

        if (
            thumbs_close
            and indexes_close
            and hands_close
        ):
            return True

        return False