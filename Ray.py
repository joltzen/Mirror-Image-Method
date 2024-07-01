import numpy.linalg as lin


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        normalized_d = direction / lin.norm(direction)
        self.direction = normalized_d
