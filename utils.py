import numpy.linalg as lin
import numpy as np

class Ray:
    """A ray object that can be shot from a source."""
    def __init__(self, origin, direction, energy=1.0):
        self.origin = origin
        self.direction = direction / lin.norm(direction)
        self.energy = energy
        self.energy_loss = 0.0
        self.hit_location = None

    #Powered by ChatGPT
    def generate_rays(n):
        """Generate n rays in a hemisphere."""
        indices = np.arange(0, n, dtype=float) + 0.5
        phi = np.arccos(1 - 2 * indices / n)
        theta = np.pi * (1 + 5**0.5) * indices

        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)

        directions = np.stack((x, y, z), axis=-1)
        return directions
    
    #Powered by ChatGPT
    def generate_random_rays(origin, n, initial_energy=1.0):
        """Generate n random rays in a hemisphere with specified initial energy."""
        z = 2 * np.random.rand(n) - 1
        t = 2 * np.pi * np.random.rand(n)
        r = np.sqrt(1 - z**2)

        x = r * np.cos(t)
        y = r * np.sin(t)

        directions = np.stack((x, y, z), axis=-1)
        return [Ray(origin, direction, initial_energy) for direction in directions]
    
    def reflect(self, reflection_coefficient):
        self.energy *= reflection_coefficient

    def apply_energy_loss(self, distance):
        if distance > 0:
            self.energy_loss = self.energy / (distance)**2

class Target:
    """A target object that can be hit by a ray."""
    def __init__(self, position, radius: float):
        
        self.position = position
        self.radius = radius

    def is_hitted_by_ray(self, ray: Ray):
        """Check if a ray hits the target."""
        #Verbindung zwischen Startpunkt Ray und Zentrum der Kugel
        a = self.position - ray.origin
        u = np.dot(a, ray.direction) / np.dot(ray.direction, ray.direction)
        p = ray.origin + u * ray.direction
        
        d = self.position - p
        hit = lin.norm(d) <= self.radius
        if hit:
            ray.hit_location = p
        return hit
    
    def set_hit_location(self, ray: Ray):
        """Set the hit location of the ray on the target."""
        a = self.position - ray.origin
        u = np.dot(a, ray.direction) / np.dot(ray.direction, ray.direction)
        p = ray.origin + u * ray.direction
        ray.hit_location = p
    def generate_random_coordinates():
        """Generate random coordinates in a unit cube."""
        x = np.random.uniform(*(0,5))
        y = np.random.uniform(*(0,5))
        z = np.random.uniform(*(0,5))
        return np.array([x, y, z])
class SoundPath:
    """A path of sound rays."""
    def __init__(self):
        self.travelPath = []

    def add_ray(self, origin, direction, reflection_point=None, order=0, face_index=None, energy=1.0, hit_location=None):
        """Add a ray to the path."""
        direction = direction / lin.norm(direction) 

        if reflection_point is not None:
            distance = lin.norm(origin - reflection_point)
        if hit_location is not None:
            distance = lin.norm(origin - hit_location)

        ray = Ray(origin, direction, energy)
        ray.apply_energy_loss(distance)
        self.travelPath.append({
            "origin": origin,
            "direction": direction,
            "reflection_point": reflection_point,
            "order": order, 
            "distance": distance,
            "face_index": face_index,
            "energy": ray.energy,
            "energy_loss":  ray.energy_loss,
            "hit_location": hit_location
        })

    def calculate_travel_time(self, speed_of_sound=343.0):
        """Calculate the total travel time of the path."""
        total_distance = 0.0
        for ray in self.travelPath:
            if ray["reflection_point"] is not None:
                total_distance += lin.norm(ray["origin"] - ray["reflection_point"])
        return total_distance / speed_of_sound
    
    def calculate_total_travel_time(self, speed_of_sound=343.0):
        """Calculate the total travel time of the path."""
        total_distance = sum(ray["distance"] for ray in self.travelPath if ray["distance"] > 0)
        if not self.travelPath or total_distance == 0:
            return 0.0
        return total_distance / speed_of_sound
    
    def calculate_energy_loss(self):
        """Calculate the total energy loss of the path."""
        if not self.travelPath:
            return 0.0
        return self.travelPath[-1]["energy_loss"]
    
    def calculate_energy_loss_of_all(self):
        """Calculate the total energy loss of the path."""
        total_distance = sum(ray["distance"] for ray in self.travelPath if ray["distance"] > 0)
        if not self.travelPath or total_distance == 0:
            return 0.0
        return self.travelPath[0]["energy"] / (total_distance)**2
    
    def __repr__(self):
        return f"Path with {len(self.travelPath)} rays."
