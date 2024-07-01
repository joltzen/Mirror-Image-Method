import trimesh
import numpy as np
import numpy.linalg as lin
from Ray import Ray

class MirrorImageMethod:
    def __init__(self, file_path, source, target, order):
        self.mesh = trimesh.load_mesh(file_path)
        self.source = source
        self.target = target
        self.order = order

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

    
    def shootRay(self, r_origin, r_direction):
        locations, index_ray, index_triangle = self.mesh.ray.intersects_location([r_origin], [r_direction])
        return locations, index_triangle
    
    
    def calculatePaths(self):
        
        for index in range(self.order):
            locations, index_triangle = self.shootRay(self.source, [0,1,0])

            if(len(locations) > 0):
                mirroredSource = self.mirror_source(index_triangle[0])

                direction = locations[0] - mirroredSource

                first_Order_reflection, _ = self.shootRay(locations[0], direction)



        

    def singleRay(self, ray: Ray):
        for index, face in enumerate(self.mesh.faces):
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


            return (intersection, index)
        
        return -1, -1


            



        
