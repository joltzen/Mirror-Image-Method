import trimesh
import numpy as np
import numpy.linalg as lin
from utils import Ray, Target, SoundPath


class MirrorImageMethod:
    def __init__(
        self,
        file_path: str,
        source: np.ndarray,
        target: Target,
        order: int,
        reflection_coefficient: float,
        initial_rays: int,
    ):
        self.mesh = trimesh.load_mesh(file_path)
        self.source = source
        self.order = order
        self.target = target
        self.reflection_coefficient = reflection_coefficient
        self.image_sources = self.find_image_sources(source, order, current_order=order)
        self.initial_rays = initial_rays
        self.paths = self.calculate_paths()
        

    def calculate_normal(self, face):
        """Calculate the normal of a face."""
        v0, v1, v2 = self.mesh.vertices[face]
        e0 = v1 - v0
        e1 = v2 - v0
        normal = np.cross(e0, e1)
        return normal / lin.norm(normal)

    def centroid_of_face(self, face):
        """Calculate the centroid of a face."""
        v0, v1, v2 = self.mesh.vertices[face]
        return np.mean([v0, v1, v2], axis=0)

    def mirror_source(self, source, face):
        """Calculate the mirrored source of a face."""
        centroid = self.centroid_of_face(face)
        r = centroid - source
        normal = self.calculate_normal(face)
        orthogonal = np.dot(r, normal) * normal
        return 2 * orthogonal + source

    def find_image_sources(self, source, order, current_order):
        """Find the image sources."""
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

    def shoot_ray(self, r_origin, r_direction):
        """Shoot a ray and return the hit location and face index."""
        locations, _, index_triangle = self.mesh.ray.intersects_location(
            [r_origin], [r_direction]
        )
        return locations, index_triangle

    def calculate_paths(self):
        """Calculate the paths of the sound waves."""
        paths = {i: [] for i in range(self.order + 1)}

        while not any(paths.values()):  # Repeat until at least one path hits the target
            initial_rays = Ray.generate_random_rays(self.source, self.initial_rays)

            for ray in initial_rays:
                path = SoundPath()
                current_ray = ray
                current_order = 0
                while current_order <= self.order:
                    locations, index_triangle = self.shoot_ray(
                        current_ray.origin, current_ray.direction
                    )
                    if not locations.size:
                        break

                    hit_location = locations[0]
                    face_index = index_triangle[0]
                    mirrored_source, _ = self.image_sources[index_triangle[0]]

                    if self.target.is_hitted_by_ray(current_ray):
                        if (
                            np.dot(
                                current_ray.direction,
                                self.target.position - current_ray.origin,
                            )
                            > 0
                        ):
                            self.target.set_hit_location(current_ray)
                            path.add_ray(
                                current_ray.origin,
                                current_ray.direction,
                                hit_location,
                                current_order,
                                face_index,
                                current_ray.energy,
                                current_ray.hit_location,
                            )
                            paths[current_order].append(path)
                            break
                    else:
                        path.add_ray(
                            current_ray.origin,
                            current_ray.direction,
                            hit_location,
                            current_order,
                            face_index,
                            current_ray.energy,
                            None,
                        )

                    reflection_direction = hit_location - mirrored_source
                    reflection_direction /= lin.norm(reflection_direction)
                    current_ray = Ray(
                        hit_location, reflection_direction, current_ray.energy
                    )
                    current_order += 1

        return paths
