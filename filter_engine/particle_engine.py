import random
import math
import time


class ParticleEngine:

    def __init__(self):

        self.hearts = []
        self.last_spawn_time = 0

        # Time between heart spawns
        self.spawn_interval = 0.12

        # Maximum number of hearts on screen
        self.max_hearts = 35

    def create_heart(self, x, y):

        current_time = time.time()

        # Control how frequently hearts are created
        if current_time - self.last_spawn_time < self.spawn_interval:
            return

        # Prevent too many hearts from accumulating
        if len(self.hearts) >= self.max_hearts:
            return

        heart = {
            "x": x + random.randint(-70, 70),
            "y": y + random.randint(-25, 25),

            "size": random.randint(10, 24),

            "speed": random.uniform(1.0, 2.8),

            "drift": random.uniform(-0.7, 0.7),

            "phase": random.uniform(0, math.pi * 2),

            "life": random.randint(55, 90),

            "max_life": 90
        }

        self.hearts.append(heart)

        self.last_spawn_time = current_time

    def update(self):

        for heart in self.hearts:

            # Move upward
            heart["y"] -= heart["speed"]

            # Add gentle sideways movement
            heart["phase"] += 0.08

            heart["x"] += (
                heart["drift"]
                + math.sin(heart["phase"]) * 0.5
            )

            # Reduce remaining lifetime
            heart["life"] -= 1

        # Remove expired hearts
        self.hearts = [
            heart
            for heart in self.hearts
            if heart["life"] > 0
        ]

