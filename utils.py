import numpy.linalg as lin
import numpy as np


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        normalized_d = direction / lin.norm(direction)
        self.direction = normalized_d

class Target:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def isHittedByRay(self, ray: Ray, hitLocation):
        #Verbindung zwischen Startpunkt Ray und Zentrum der Kugel
        a = self.position - ray.origin

        u = np.dot(a, ray.direction) / np.dot(ray.direction, ray.direction)

        P = ray.origin + u * ray.direction
        d = self.position - P

        lenght_of_d = lin.norm(d)

        if(lenght_of_d <= self.radius):
            return True
        
        return False
