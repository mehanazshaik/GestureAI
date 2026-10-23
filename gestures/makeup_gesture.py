import time


class GhostGesture:

    def __init__(self):

        self.previous_gesture = "No Hand"
        self.transition_time = 0

        self.cooldown = 1.5
        self.last_ghost_time = 0

    def detect(self, gesture):

        current_time = time.time()

        # Check for Open Palm → Fist
        if (
            self.previous_gesture == "Open Palm"
            and gesture == "Fist"
        ):

            if current_time - self.last_ghost_time > self.cooldown:

                self.last_ghost_time = current_time

                self.previous_gesture = gesture

                return True

        self.previous_gesture = gesture

        return False