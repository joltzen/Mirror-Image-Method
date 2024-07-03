import numpy.linalg as lin
import numpy as np


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        normalized_d = direction / lin.norm(direction)
        self.direction = normalized_d

    #Powered by ChatGPT
    def generate_rays(numberOfRays):
        indices = np.arange(0, numberOfRays, dtype=float) + 0.5

        phi = np.arccos(1 - 2*indices/numberOfRays)
        theta = np.pi * (1 + 5**0.5) * indices

        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)

        directions = np.stack((x, y, z), axis=-1)
        return directions
    
    #Powered by ChatGPT
    def generate_random_rays(origin, n):
        z = 2 * np.random.rand(n) - 1
        t = 2 * np.pi * np.random.rand(n)
        r = np.sqrt(1 - z**2)
        
        x = r * np.cos(t)
        y = r * np.sin(t)
        
        directions = np.stack((x, y, z), axis=-1)
        return [Ray(origin, direction) for direction in directions]

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
