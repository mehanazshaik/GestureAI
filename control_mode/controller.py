import cv2
import time


class GestureController:

    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 1.0

    def can_trigger(self):
        current_time = time.time()

        if current_time - self.last_action_time >= self.cooldown:
            self.last_action_time = current_time
            return True

        return False

    def take_screenshot(self, frame):

        if not self.can_trigger():
            return

        filename = time.strftime(
            "gesture_screenshot_%Y%m%d_%H%M%S.png"
        )

        cv2.imwrite(filename, frame)

        print(f"📸 Screenshot saved: {filename}")