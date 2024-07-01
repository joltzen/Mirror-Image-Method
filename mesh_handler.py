import trimesh
import numpy as np
import numpy.linalg as lin
from Ray import Ray
from collections import namedtuple

class MeshHandler:
    def __init__(self, file_path):
        self.mesh = trimesh.load_mesh(file_path)

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
        orthogonal = (np.dot(r, normal) * np.dot(normal, normal) * normal)
        return 2 * orthogonal + source

    def find_image_sources(self, source, order, current_order=1):
        if current_order > order:
            return []
        image_sources = []
        for face in self.mesh.faces:
            mirrored_source = self.mirror_source(source, face)
            image_sources.append((mirrored_source, current_order))
            image_sources.extend(self.find_image_sources(mirrored_source, order, current_order + 1))
        return image_sources

    def angle_between_vectors(self, a, b):
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        cos_theta = dot_product / (norm_a * norm_b)
        return np.arccos(np.clip(cos_theta, -1.0, 1.0))
    
    def shootRay(self, r_origin, r_direction):
        locations, index_ray, index_triangle = self.mesh.ray.intersects_location([r_origin], [r_direction])
        print("Locations: ", locations)
        print("index_ray: ", index_ray)
        print("index_triangle: ", index_triangle)
        return locations
    
    def singleRay(self, ray: Ray):
        for face in self.mesh.faces:
            v0, v1, v2 = self.mesh.vertices[face]
            e0 = v1 - v0
            e1 = v2 - v0
            s = ray.origin - v0

            q2 = lin.cross(ray.direction, e1)
            q1 = lin.cross(s, e0)

            if(np.abs(np.dot(q2,e0)) <= 0.00005):
                continue
            

            t = np.dot(q1, e1)
            beta = np.dot(q2,s)
            gamma = np.dot(q1,ray.direction)

            result = (1/np.dot(q2,e0))*np.array([t, beta, gamma])

            if(result[1] < 0):
                continue

            if(result[2] < 0):
                continue

            if(result[1] + result[2] > 1):
                continue
            
            intersection = ((1-result[1]-result[2])*v0)+result[1]*v1+result[2]*v2


            return (intersection, face)
        
        return -1, -1


            



        
