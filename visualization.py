# visualization.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from utils import Target, Ray
from mirror_image_method import MirrorImageMethod


class MeshVisualizer:
    def __init__(self, room : MirrorImageMethod):
        self.room = room
        self.source_point = room.source
        self.reflections_order = room.order
        self.mirrored_sources = room.find_image_sources(self.source_point, self.reflections_order)
        self.target = room.target
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_box_aspect([1,1,1])

    def show(self):
        self.ax.set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.ax.set_title("3D Points Plot")
        plt.show()

    def plot_vertices(self):
        """Plot the vertices of the mesh."""
        mesh = self.room.mesh
        x, y, z = mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2]
        self.ax.scatter(x, y, z, c="black", marker="o")

    def plot_faces(self, highlightFace:int = None):
        """Plot the faces of the mesh."""
        if highlightFace is None:
            highlightFace = float('inf')

        mesh = self.room.mesh
        for index, face in enumerate(mesh.faces):
            color = "black" if index != highlightFace else "red"
            for i in range(3):
                self.ax.plot(
                    [mesh.vertices[face[i], 0], mesh.vertices[face[(i + 1) % 3], 0]],
                    [mesh.vertices[face[i], 1], mesh.vertices[face[(i + 1) % 3], 1]],
                    [mesh.vertices[face[i], 2], mesh.vertices[face[(i + 1) % 3], 2]],
                    c=color,
                    alpha=0.1 if index != highlightFace else 1.0,
                )



    def plot_mirrored_sources(self):
        for point, order in self.mirrored_sources:
            self.ax.scatter(point[0], point[1], point[2], color="red")

    # def plot_mirrored_sources(self):
    #     """Plot the image sources."""
    #     mesh = self.room.mesh
    #     ps = self.source_point

    #     if self.target_face < len(mesh.faces):
    #         face = mesh.faces[self.target_face]
    #         center = self.room.centroid_of_face(face)
    #         r = center - ps
    #         normal = self.room.calculate_normal(face)
    #         orthogonal = np.dot(r, normal) * np.dot(normal, normal) * normal
    #         mirrored_source = self.room.mirror_source(ps, face)

    #         # self.ax.quiver(ps[0], ps[1], ps[2], r[0], r[1], r[2], color="green")
    #         # self.ax.text(ps[0] + r[0]/2, ps[1] + r[1]/2, ps[2] + r[2]/2, 'R', color='green')
    #         # self.ax.quiver(center[0], center[1], center[2], normal[0], normal[1], normal[2], color="red", alpha=0.2)
    #         # self.ax.text(center[0] + normal[0]/2, center[1] + normal[1]/2, center[2] + normal[2]/2, 'n', color='red')
    #         # self.ax.quiver(ps[0], ps[1], ps[2], orthogonal[0], orthogonal[1], orthogonal[2], color="purple")
    #         # self.ax.text(ps[0] + orthogonal[0]/2, ps[1] + orthogonal[1]/2, ps[2] + orthogonal[2]/2, 'n|r|cos(alpha)', color='purple')
    #         # self.ax.scatter(mirrored_source[0], mirrored_source[1], mirrored_source[2], c="orange")
    #         # self.ax.text(mirrored_source[0], mirrored_source[1], mirrored_source[2], 'I', color='orange')

    def plot_reflections(self):
        """Plot the reflections of the mesh."""
        ps = self.source_point
        random_rays = Ray.generate_random_rays(ps, 10)
        hit_target = False

        for ray in random_rays:
            # Shoot the ray from the source point
            locations, index_triangle = self.room.shootRay(ray.origin, ray.direction)

            if locations.shape[0] > 0:
                hit_location = locations[0]
                mirrored_source, order = self.image_sources[index_triangle[0]]

                # Plot the original ray
                self.ax.quiver(ray.origin[0], ray.origin[1], ray.origin[2], ray.direction[0], ray.direction[1], ray.direction[2], color="blue")
                self.ax.scatter(hit_location[0], hit_location[1], hit_location[2], c="orange")

                # Check if the target is hit by the original ray
                is_hitted = self.target.isHittedByRay(ray, hit_location)
                print(f"Ray {ray.direction} hits target? {is_hitted}")

                if is_hitted:
                    self.ax.scatter(self.target.position[0], self.target.position[1], self.target.position[2], color="magenta", label="Target")
                    print("Target hit")
                    hit_target = True
                    break
                else:
                    print("Target miss")

                    # Calculate reflection direction
                    reflection_direction = hit_location - mirrored_source
                    reflection_direction /= np.linalg.norm(reflection_direction)  # Normalize the direction

                    # Shoot the reflected ray from the hit location
                    reflection_locations, _ = self.room.shootRay(hit_location, reflection_direction)

                    if reflection_locations.shape[0] > 0:
                        reflection_hit_location = reflection_locations[0]

                        # Plot the reflected ray
                        self.ax.quiver(hit_location[0], hit_location[1], hit_location[2], reflection_direction[0], reflection_direction[1], reflection_direction[2], color="red")
                        self.ax.scatter(reflection_hit_location[0], reflection_hit_location[1], reflection_hit_location[2], c="green")

                        # Check if the target is hit by the reflected ray
                        reflected_ray = Ray(hit_location, reflection_direction)
                        is_hitted = self.target.isHittedByRay(reflected_ray, reflection_hit_location)
                        print(f"Second Ray {reflection_direction} hits target? {is_hitted}")

                        if is_hitted:
                            self.ax.scatter(self.target.position[0], self.target.position[1], self.target.position[2], color="magenta", label="Target")
                            print("Target hit by first order reflection")
                            hit_target = True
                            break
                        else:
                            print("Target miss by first order reflection")

        if not hit_target:
            print("No rays hit the target.")
            