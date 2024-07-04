import trimesh
import numpy as np
import numpy.linalg as lin
from utils import Ray, Target, Path


class MirrorImageMethod:
    def __init__(self, file_path:str, source, target: Target, order: int):
        self.mesh = trimesh.load_mesh(file_path)
        self.source = source
        self.order = order
        self.target = target
        self.image_sources = self.find_image_sources(
            source, order
        )
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

    def shootRay(self, r_origin, r_direction):
        locations, index_ray, index_triangle = self.mesh.ray.intersects_location(
            [r_origin], [r_direction]
        )
        return locations, index_triangle

    def calculatePaths(self):
        paths = []
        initial_rays = Ray.generate_random_rays(self.source, 100)  
        
        for ray in initial_rays:
            path = Path()
            current_ray = ray
            current_order = 0
            while current_order <= self.order:
                locations, index_triangle = self.shootRay(current_ray.origin, current_ray.direction)
                if len(locations) == 0:
                    break

                hit_location = locations[0]
                mirrored_source, order = self.image_sources[index_triangle[0]]
                path.addRay(current_ray.origin, current_ray.direction, hit_location, current_order)

                is_hitted = self.target.isHittedByRay(ray, hit_location)

                if is_hitted:
                    paths.append(path)
                    break

                reflection_direction = hit_location - mirrored_source
                reflection_direction /= np.linalg.norm(reflection_direction)
                reflection_locations, _ = self.shootRay(hit_location, reflection_direction)
                
                if reflection_locations.shape[0] > 0:
                    current_order += 1
                    reflection_hit_location = reflection_locations[0]
                    current_ray = Ray(hit_location, reflection_direction)
                    is_hitted = self.target.isHittedByRay(current_ray, reflection_hit_location)
                    path.addRay(current_ray.origin, current_ray.direction, reflection_hit_location, current_order)

                    if is_hitted:
                            paths.append(path)
                            break

        return paths
            

    def singleRay(self, ray: Ray):
        for index, face in enumerate(self.mesh.faces):
            v0, v1, v2 = self.mesh.vertices[face]
            e0 = v1 - v0
            e1 = v2 - v0
            s = ray.origin - v0

            q2 = lin.cross(ray.direction, e1)
            q1 = lin.cross(s, e0)

            if np.abs(np.dot(q2, e0)) <= 0.00005:
                continue

            t = np.dot(q1, e1)
            beta = np.dot(q2, s)
            gamma = np.dot(q1, ray.direction)

            result = (1 / np.dot(q2, e0)) * np.array([t, beta, gamma])

            if result[1] < 0:
                continue

            if result[2] < 0:
                continue

            if result[1] + result[2] > 1:
                continue

            intersection = (
                ((1 - result[1] - result[2]) * v0) + result[1] * v1 + result[2] * v2
            )

            return (intersection, index)

        return -1, -1
    
        
