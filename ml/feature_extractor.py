import math


class FeatureExtractor:

    def extract(self, landmarks):

        if not landmarks:
            return []

        features = []

        # Wrist is our reference point
        wrist_x = landmarks[0][0]
        wrist_y = landmarks[0][1]

        for point in landmarks:

            x = point[0]
            y = point[1]

            # Move coordinates relative to wrist
            relative_x = x - wrist_x
            relative_y = y - wrist_y

            features.append(relative_x)
            features.append(relative_y)

        return features