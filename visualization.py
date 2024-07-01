# visualization.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class MeshVisualizer:
    def __init__(self, mesh_handler, source_point, reflections_order, target_face):
        self.mesh_handler = mesh_handler
        self.source_point = source_point
        self.reflections_order = reflections_order
        self.target_face = target_face
        self.image_sources = mesh_handler.find_image_sources(
            source_point, reflections_order
        )

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
        mesh = self.mesh_handler.mesh
        x, y, z = mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2]
        ax.scatter(x, y, z, c="black", marker="o")
        ax.scatter(
            self.source_point[0], self.source_point[1], self.source_point[2], c="blue"
        )
        ax.text(
            self.source_point[0],
            self.source_point[1],
            self.source_point[2],
            "S",
            color="blue",
        )

    def plot_faces(self, ax):
        """Plot the faces of the mesh."""
        mesh = self.mesh_handler.mesh
        for index, face in enumerate(mesh.faces):
            color = "black" if index != self.target_face else "red"
            for i in range(3):
                ax.plot(
                    [mesh.vertices[face[i], 0], mesh.vertices[face[(i + 1) % 3], 0]],
                    [mesh.vertices[face[i], 1], mesh.vertices[face[(i + 1) % 3], 1]],
                    [mesh.vertices[face[i], 2], mesh.vertices[face[(i + 1) % 3], 2]],
                    c=color,
                    alpha=0.1 if index != self.target_face else 1.0,
                )
            mirrored_ps = self.mesh_handler.mirror_source(self.source_point, face)
            ax.scatter(
                mirrored_ps[0],
                mirrored_ps[1],
                mirrored_ps[2],
                c="pink" if index != self.target_face else "orange",
            )

    def plot_image_sources(self, ax):
        """Plot the image sources."""
        mesh = self.mesh_handler.mesh
        ps = self.source_point

        if self.target_face < len(mesh.faces):
            face = mesh.faces[self.target_face]
            center = self.mesh_handler.centroid_of_face(face)
            r = center - ps
            normal = self.mesh_handler.calculate_normal(face)
            orthogonal = np.dot(r, normal) * np.dot(normal, normal) * normal
            mirrored_source = self.mesh_handler.mirror_source(ps, face)

            # ax.quiver(ps[0], ps[1], ps[2], r[0], r[1], r[2], color="green")
            # ax.text(ps[0] + r[0]/2, ps[1] + r[1]/2, ps[2] + r[2]/2, 'R', color='green')
            # ax.quiver(center[0], center[1], center[2], normal[0], normal[1], normal[2], color="red", alpha=0.2)
            # ax.text(center[0] + normal[0]/2, center[1] + normal[1]/2, center[2] + normal[2]/2, 'n', color='red')
            # ax.quiver(ps[0], ps[1], ps[2], orthogonal[0], orthogonal[1], orthogonal[2], color="purple")
            # ax.text(ps[0] + orthogonal[0]/2, ps[1] + orthogonal[1]/2, ps[2] + orthogonal[2]/2, 'n|r|cos(alpha)', color='purple')
            # ax.scatter(mirrored_source[0], mirrored_source[1], mirrored_source[2], c="orange")
            # ax.text(mirrored_source[0], mirrored_source[1], mirrored_source[2], 'I', color='orange')

    def plot_reflections(self, ax):
        """Plot the reflections of the mesh."""
        ps = self.source_point
        direction = np.array([0.35, 0.5, 0.2])
        locations, index_triangle = self.mesh_handler.shootRay(
            self.source_point, direction
        )
        mirrored_source, order = self.image_sources[index_triangle[0]]

        ax.quiver(
            ps[0], ps[1], ps[2], direction[0], direction[1], direction[2], color="blue"
        )
        ax.scatter(locations[0, 0], locations[0, 1], locations[0, 2], c="green")

        reflection_direction = locations[0] - mirrored_source
        first_order_reflection, test = self.mesh_handler.shootRay(
            np.add(locations[0], -0.0005), reflection_direction
        )

        ax.quiver(
            locations[0, 0],
            locations[0, 1],
            locations[0, 2],
            reflection_direction[0],
            reflection_direction[1],
            reflection_direction[2],
            color="green",
        )
        ax.scatter(
            first_order_reflection[0, 0],
            first_order_reflection[0, 1],
            first_order_reflection[0, 2],
            color="orange",
        )
        print(first_order_reflection)
