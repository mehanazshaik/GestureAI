import time


class SwipeDetector:

    def __init__(self):

        # Store recent wrist positions
        self.history = []

        # Number of positions to remember
        self.max_history = 10

        # Minimum horizontal movement
        self.threshold = 50

        # Minimum horizontal movement compared to vertical movement
        self.direction_ratio = 1.5

        # Prevent repeated detection
        self.cooldown = 0.7

        self.last_swipe_time = 0

    def detect(self, landmarks):

        if not landmarks:
            self.history = []
            return None

        # Wrist position
        wrist_x = landmarks[0][0]
        wrist_y = landmarks[0][1]

        current_time = time.time()

        # Add current position
        self.history.append(
            (wrist_x, wrist_y, current_time)
        )

        # Keep only recent positions
        if len(self.history) > self.max_history:
            self.history.pop(0)

        # Need enough movement points
        if len(self.history) < 3:
            return None

        # Check cooldown
        if current_time - self.last_swipe_time < self.cooldown:
            return None

        # Oldest position
        start_x = self.history[0][0]
        start_y = self.history[0][1]

        # Current position
        end_x = self.history[-1][0]
        end_y = self.history[-1][1]

        # Calculate movement
        movement_x = end_x - start_x
        movement_y = end_y - start_y

        # --------------------------------
        # SWIPE RIGHT
        # --------------------------------

        if (
            movement_x > self.threshold
            and abs(movement_x) > abs(movement_y) * self.direction_ratio
        ):

            self.last_swipe_time = current_time
            self.history = []

            return "Swipe Right"

        # --------------------------------
        # SWIPE LEFT
        # --------------------------------

        if (
            movement_x < -self.threshold
            and abs(movement_x) > abs(movement_y) * self.direction_ratio
        ):

            self.last_swipe_time = current_time
            self.history = []

            return "Swipe Left"

        return None