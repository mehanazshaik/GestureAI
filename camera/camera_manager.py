import cv2


class CameraManager:

    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def start(self):

        if not self.camera.isOpened():
            print("Error: Could not open camera.")
            return

        print("Camera started.")
        print("Press Q to quit.")

        while True:

            success, frame = self.camera.read()

            if not success:
                print("Error: Could not read frame.")
                break

            cv2.imshow("GestureAR Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.camera.release()
        cv2.destroyAllWindows()