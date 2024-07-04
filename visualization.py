# visualization.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from utils import Target, Ray
from mirror_image_method import MirrorImageMethod


class MeshVisualizer:
    def __init__(self, room : MirrorImageMethod):
        self.room = room
        self.mirrored_sources = room.find_image_sources(self.room.source, self.room.order)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_box_aspect([1,1,1])

    def show(self):
        self.ax.set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.ax.set_title("3D Points Plot")
        self.fig.canvas.mpl_connect('key_press_event', lambda event: plt.close(self.fig) if event.key == "escape" else None)
        plt.show()

    def plot_ray_path(self):
        
        for path in self.room.paths:
            origin = path.ray.origin
            endPoint = path.ray.getEndPoint()

            self.ax.quiver(origin[0], origin[1], origin[2], endPoint[0],endPoint[1],endPoint[2],  color="green")

    def plot_target(self):
        u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
        x = self.room.target.position[0] + (self.room.target.radius/2) * np.cos(u) * np.sin(v)
        y = self.room.target.position[1] + (self.room.target.radius/2) * np.sin(u) * np.sin(v)
        z = self.room.target.position[2] + (self.room.target.radius/2) * np.cos(v)
        self.ax.plot_surface(x, y, z, color="blue", alpha=0.1)

    def plot_point(self, point):
        self.ax.scatter(point[0], point[1], point[2], color="magenta")

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
    #     ps = self.room.source

    #     if self.room.target_face < len(mesh.faces):
    #         face = mesh.faces[self.room.target_face]
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

    