from typing import List
import trimesh
import numpy as np
import numpy.linalg as lin
from utils import Ray, Target, SoundPath


class MirrorImageMethod:
    def __init__(self, file_path:str, source, target: Target, order: int):
        self.mesh = trimesh.load_mesh(file_path)
        self.source = source
        self.order = order
        self.target = target
        self.paths:List[SoundPath] = []

    def calculate_normal(self, face):
        v0, v1, v2 = self.mesh.vertices[face]
        e0 = v1 - v0
        e1 = v2 - v0
        normal = np.cross(e0, e1)
        normal = normal / lin.norm(normal)
        return normal

    def centroid_of_face(self, face):
        v0, v1, v2 = self.mesh.vertices[face]
        return np.mean([v0, v1, v2], axis=0)

    def mirror_source(self, source, face):
        centroid = self.centroid_of_face(face)
        r = centroid - source
        normal = self.calculate_normal(face)
        orthogonal = np.dot(r, normal) * np.dot(normal, normal) * normal
        return 2 * orthogonal + source

    def find_image_sources(self, source, order, current_order=1):
        if current_order > order:
            return []
        image_sources = []
        for face in self.mesh.faces:
            mirrored_source = self.mirror_source(source, face)
            image_sources.append((mirrored_source, current_order))
            image_sources.extend(
                self.find_image_sources(mirrored_source, order, current_order + 1)
            )
        return image_sources

    def shootRay(self, ray:Ray):
        locations, index_ray, index_triangle = self.mesh.ray.intersects_location([ray.origin], [ray.direction])
        return locations, index_triangle
    
    def simulate(self, numberOfRays: int):
        #1. Generate initial rays
        rays = Ray.generate_rays(self.source, numberOfRays)

        for ray in rays:
            #2. Calculate the intersection with the face
            hitLocation, index_triangle = self.shootRay(ray)
            ray.lenght = lin.norm(hitLocation - ray.origin)

            #3. Test wether the ray hits only a surface or the target
            if self.target.isHittedByRay(ray, hitLocation):
                self.paths.append(SoundPath(ray, 1))
                print("Target hitted")
                continue
                

            #4. If target: store the ray and don't reflect it 

            #5. If surface: repeat the reflection another time (but just n = order times)

    # def plot_reflections(self, numberOfRays: int):
    #     """Plot the reflections of the mesh."""        
    #     random_rays = Ray.generate_random_rays(self.source, numberOfRays)
    #     hit_target = False

    #     for ray in random_rays:
    #         # Shoot the ray from the source point
    #         locations, index_triangle = self.room.shootRay(ray.origin, ray.direction)

    #         if locations.shape[0] > 0:
    #             hit_location = locations[0]
    #             mirrored_source, order = self.image_sources[index_triangle[0]]

    #             # Check if the target is hit by the original ray
    #             is_hitted = self.room.target.isHittedByRay(ray, hit_location)
    #             print(f"Ray {ray.direction} hits target? {is_hitted}")

    #             if is_hitted:
    #                 print("Target hit")
    #                 hit_target = True
    #                 break
    #             else:
    #                 print("Target miss")

    #                 # Calculate reflection direction
    #                 reflection_direction = hit_location - mirrored_source
    #                 reflection_direction /= np.linalg.norm(reflection_direction)  # Normalize the direction

    #                 # Shoot the reflected ray from the hit location
    #                 reflection_locations, _ = self.room.shootRay(hit_location, reflection_direction)

    #                 if reflection_locations.shape[0] > 0:
    #                     reflection_hit_location = reflection_locations[0]


    #                     # Check if the target is hit by the reflected ray
    #                     reflected_ray = Ray(hit_location, reflection_direction)
    #                     is_hitted = self.room.target.isHittedByRay(reflected_ray, reflection_hit_location)
    #                     print(f"Second Ray {reflection_direction} hits target? {is_hitted}")

    #                     if is_hitted:
    #                         print("Target hit by first order reflection")
    #                         hit_target = True
    #                         break
    #                     else:
    #                         print("Target miss by first order reflection")

    #     if not hit_target:
    #         print("No rays hit the target.")

    # def singleRay(self, ray: Ray):
    #     for index, face in enumerate(self.mesh.faces):
    #         v0, v1, v2 = self.mesh.vertices[face]
    #         e0 = v1 - v0
    #         e1 = v2 - v0
    #         s = ray.origin - v0

    #         q2 = lin.cross(ray.direction, e1)
    #         q1 = lin.cross(s, e0)

    #         if np.abs(np.dot(q2, e0)) <= 0.00005:
    #             continue

    #         t = np.dot(q1, e1)
    #         beta = np.dot(q2, s)
    #         gamma = np.dot(q1, ray.direction)

    #         result = (1 / np.dot(q2, e0)) * np.array([t, beta, gamma])

    #         if result[1] < 0:
    #             continue

    #         if result[2] < 0:
    #             continue

    #         if result[1] + result[2] > 1:
    #             continue

    #         intersection = (
    #             ((1 - result[1] - result[2]) * v0) + result[1] * v1 + result[2] * v2
    #         )

    #         return (intersection, index)

    #     return -1, -1
    
        
