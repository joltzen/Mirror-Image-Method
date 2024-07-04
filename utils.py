import numpy.linalg as lin
import numpy as np

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction / lin.norm(direction)

    #Powered by ChatGPT
    def generate_rays(number_of_rays):
        indices = np.arange(0, number_of_rays, dtype=float) + 0.5
        phi = np.arccos(1 - 2 * indices / number_of_rays)
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
    def __init__(self, position, radius: float):
        self.position = position
        self.radius = radius

    def is_hitted_by_ray(self, ray: Ray, hitLocation):
        #Verbindung zwischen Startpunkt Ray und Zentrum der Kugel
        a = self.position - ray.origin
        u = np.dot(a, ray.direction) / np.dot(ray.direction, ray.direction)
        p = ray.origin + u * ray.direction
        d = self.position - p

        return lin.norm(d) <= self.radius

class SoundPath:
    def __init__(self):
        self.rays = []

    def add_ray(self, origin, direction, reflection_point=None, order=0, face_index=None):
        self.rays.append({
            "origin": origin,
            "direction": direction,
            "reflection_point": reflection_point,
            "order": order,
            "face_index": face_index
        })

    def __repr__(self):
        return f"Path with {len(self.rays)} rays."
