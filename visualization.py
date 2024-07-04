import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from utils import Target

class MeshVisualizer:
    def __init__(self, room, target_face):
        self.room = room
        self.target_face = target_face

    def plot_mesh(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.set_box_aspect([1, 1, 1])

        self.plot_vertices(ax)
        self.plot_faces(ax)
        self.plot_image_sources(ax)
        self.plot_reflections(ax)

        ax.set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax.set_title("3D Points Plot")
        plt.show()

    def plot_vertices(self, ax):
        """Plot the vertices of the mesh."""
        mesh = self.room.mesh
        x, y, z = mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2]
        ax.scatter(x, y, z, c="black", marker="o")
        ax.scatter(self.room.source[0], self.room.source[1], self.room.source[2], c="blue")
        ax.text(self.room.source[0], self.room.source[1], self.room.source[2], "S", color="blue")

    def plot_faces(self, ax):
        """Plot the faces of the mesh."""
        mesh = self.room.mesh
        for index, face in enumerate(mesh.faces):
            color = "black" if index != self.target_face else "red"
            for i in range(3):
                ax.plot([mesh.vertices[face[i], 0], mesh.vertices[face[(i + 1) % 3], 0]],
                        [mesh.vertices[face[i], 1], mesh.vertices[face[(i + 1) % 3], 1]],
                        [mesh.vertices[face[i], 2], mesh.vertices[face[(i + 1) % 3], 2]], c=color, alpha=0.1 if index != self.target_face else 1.0)
            mirrored_ps = self.room.mirror_source(self.room.source, face)
            ax.scatter(mirrored_ps[0], mirrored_ps[1], mirrored_ps[2], c="pink" if index != self.target_face else "orange")

    def plot_image_sources(self, ax):
        """Plot the image sources."""
        mesh = self.room.mesh
        ps = self.room.source

        if self.target_face < len(mesh.faces):
            face = mesh.faces[self.target_face]
            center = self.room.centroid_of_face(face)
            r = center - ps
            normal = self.room.calculate_normal(face)
            orthogonal = np.dot(r, normal) * normal
            mirrored_source = self.room.mirror_source(ps, face)

            ax.quiver(ps[0], ps[1], ps[2], r[0], r[1], r[2], color="green", alpha=0.2)
            ax.text(ps[0] + r[0]/2, ps[1] + r[1]/2, ps[2] + r[2]/2, 'R', color='green')
            ax.quiver(center[0], center[1], center[2], normal[0], normal[1], normal[2], color="red", alpha=0.2)
            ax.text(center[0] + normal[0]/2, center[1] + normal[1]/2, center[2] + normal[2]/2, 'n', color='red')
            ax.quiver(ps[0], ps[1], ps[2], orthogonal[0], orthogonal[1], orthogonal[2], color="purple", alpha=0.2)
            ax.text(ps[0] + orthogonal[0]/2, ps[1] + orthogonal[1]/2, ps[2] + orthogonal[2]/2, 'n|r|cos(alpha)', color='purple')
            ax.scatter(mirrored_source[0], mirrored_source[1], mirrored_source[2], c="orange", alpha=0.2)
            ax.text(mirrored_source[0], mirrored_source[1], mirrored_source[2], 'I', color='orange')

    def plot_reflections(self, ax):
        paths_dict = self.room.paths
        print("-" * 40)
        print(sum(len(paths) for paths in paths_dict.values()), "paths found.")
        print("-" * 40)

        order_colors = ['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'magenta']
        hit_colors = ['red', 'green', 'purple', 'orange', 'cyan', 'magenta', 'blue']

        for order, paths in paths_dict.items():
            for path in paths:
                travel_time = path.calculate_travel_time()
                print(f"Travel time for order {order}: {travel_time:.6f} seconds")
                for ray_info in path.rays:
                    origin = ray_info["origin"]
                    direction = ray_info["direction"]
                    reflection_point = ray_info["reflection_point"]

                    self.print_ray_info(ray_info)

                    color = order_colors[order % len(order_colors)]
                    hit_color = hit_colors[order % len(hit_colors)]
                    ax.quiver(origin[0], origin[1], origin[2], direction[0], direction[1], direction[2], color=color)

                    if reflection_point is not None:
                        ax.scatter(reflection_point[0], reflection_point[1], reflection_point[2], c=hit_color)

        if any(paths_dict.values()):
            ax.scatter(self.room.target.position[0], self.room.target.position[1], self.room.target.position[2], color="magenta", label="Target", s=self.room.target.radius * 1000)
        else:
            print("No rays hit the target.")

    def print_ray_info(self, ray_info):
        origin = ray_info["origin"]
        direction = ray_info["direction"]
        reflection_point = ray_info["reflection_point"]
        order = ray_info["order"]
        face_index = ray_info["face_index"]

        print(f"Ray Info (Order {order}):")
        print(f"  Origin: {origin}")
        print(f"  Direction: {direction}")
        print(f"  Face Index: {face_index}")
        if reflection_point is not None:
            print(f"  Reflection Point: {reflection_point}")
        else:
            print("  Reflection Point: None")
        print("-" * 40)
