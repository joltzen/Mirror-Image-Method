import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from utils import Target
import matplotlib.cm as cm


class MeshVisualizer:
    def __init__(self, room, target_face=-1):
        self.room = room
        self.target_face = target_face

    def plot_mesh(self):
        """Plot the mesh."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.set_box_aspect([1, 1, 1])

        self.plot_vertices(ax)
        self.plot_image_sources(ax)
        self.plot_reflections(ax)
        if self.target_face >= 0:
            self.plot_highlighted_target_face(ax)
        else:
            self.plot_faces(ax)
        # plot the faces with their index
        # self.identify_faces(ax)
        self.plot_target(ax)

        ax.set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax.set_title("3D Points Plot")
        plt.show()

    def plot_vertices(self, ax):
        """Plot the vertices of the mesh."""
        mesh = self.room.mesh
        x, y, z = mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2]
        ax.scatter(x, y, z, c="black", marker="o")
        ax.scatter(
            self.room.source[0], self.room.source[1], self.room.source[2], c="blue"
        )
        ax.text(
            self.room.source[0],
            self.room.source[1],
            self.room.source[2],
            "S",
            color="blue",
        )

    def plot_faces(self, ax):
        """Plot the faces of the mesh."""
        mesh = self.room.mesh
        for index, face in enumerate(mesh.faces):
            for i in range(3):
                ax.plot(
                    [mesh.vertices[face[i], 0], mesh.vertices[face[(i + 1) % 3], 0]],
                    [mesh.vertices[face[i], 1], mesh.vertices[face[(i + 1) % 3], 1]],
                    [mesh.vertices[face[i], 2], mesh.vertices[face[(i + 1) % 3], 2]],
                    c="black",
                    alpha=0.1,
                )
            mirrored_ps = self.room.mirror_source(self.room.source, face)
            ax.scatter(mirrored_ps[0], mirrored_ps[1], mirrored_ps[2], c="pink")

    def plot_highlighted_target_face(self, ax):
        """Plot the faces of the mesh."""
        mesh = self.room.mesh
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
            mirrored_ps = self.room.mirror_source(self.room.source, face)
            ax.scatter(
                mirrored_ps[0],
                mirrored_ps[1],
                mirrored_ps[2],
                c="pink" if index != self.target_face else "orange",
            )

    def identify_faces(self, ax):
        """Colors the faces and labels them with their index."""
        mesh = self.room.mesh
        num_faces = len(mesh.faces)
        colors = plt.get_cmap("tab20", num_faces)

        for index, face in enumerate(mesh.faces):
            color = colors(index / num_faces)
            for i in range(3):
                ax.plot(
                    [mesh.vertices[face[i], 0], mesh.vertices[face[(i + 1) % 3], 0]],
                    [mesh.vertices[face[i], 1], mesh.vertices[face[(i + 1) % 3], 1]],
                    [mesh.vertices[face[i], 2], mesh.vertices[face[(i + 1) % 3], 2]],
                    c=color,
                    alpha=0.6 if index != self.target_face else 1.0,
                )

            centroid = self.room.centroid_of_face(face)
            ax.text(centroid[0], centroid[1], centroid[2], str(index), color=color)
            mirrored_ps = self.room.mirror_source(self.room.source, face)
            ax.scatter(mirrored_ps[0], mirrored_ps[1], mirrored_ps[2], color=color)

    def plot_image_sources(self, ax):
        """Plot the image sources."""
        mesh = self.room.mesh
        ps = self.room.source

        if 0 <= self.target_face < len(mesh.faces):
            face = mesh.faces[self.target_face]
            center = self.room.centroid_of_face(face)
            r = center - ps
            normal = self.room.calculate_normal(face)
            orthogonal = np.dot(r, normal) * normal
            mirrored_source = self.room.mirror_source(ps, face)

            self.plot_vector(ax, ps, r, "green", "R")
            self.plot_vector(ax, center, normal, "red", "n")
            self.plot_vector(ax, ps, orthogonal, "purple", "n|r|cos(alpha)")
            ax.scatter(
                mirrored_source[0],
                mirrored_source[1],
                mirrored_source[2],
                c="orange",
                alpha=0.2,
            )
            ax.text(
                mirrored_source[0],
                mirrored_source[1],
                mirrored_source[2],
                "I",
                color="orange",
            )

    def plot_vector(self, ax, origin, vector, color, label):
        """Helper function to plot vectors with labels."""
        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            vector[0],
            vector[1],
            vector[2],
            color=color,
            alpha=0.3,
        )
        ax.text(
            origin[0] + vector[0] / 2,
            origin[1] + vector[1] / 2,
            origin[2] + vector[2] / 2,
            label,
            color=color,
        )

    def plot_target(self, ax):
        u, v = np.mgrid[0 : 2 * np.pi : 100j, 0 : np.pi : 50j]
        x = self.room.target.position[0] + (self.room.target.radius) * np.cos(
            u
        ) * np.sin(v)
        y = self.room.target.position[1] + (self.room.target.radius) * np.sin(
            u
        ) * np.sin(v)
        z = self.room.target.position[2] + (self.room.target.radius) * np.cos(v)
        ax.plot_surface(x, y, z, color="blue", alpha=0.1)

    def plot_reflections(self, ax):
        """Plot reflection paths."""
        paths_dict = self.room.paths
        total_paths = sum(len(paths) for paths in paths_dict.values())
        print("-" * 80)
        print(f"{total_paths} paths found.")

        order_colors = ["blue", "red", "green", "purple", "orange", "cyan", "magenta"]
        hit_colors = ["red", "green", "purple", "orange", "cyan", "magenta", "blue"]

        for order, paths in paths_dict.items():
            for path in paths:
                travel_time = path.calculate_total_travel_time()
                energy_loss = path.calculate_energy_loss_of_all()
                print("=" * 80)
                print(f"Travel time for order {order}: {travel_time:.6f} seconds")
                print(f"Energy loss for order {order}: {energy_loss:.6f}")
                print("=" * 80)
                for ray_info in path.travelPath:
                    self.print_ray_info(ray_info)
                    self.plot_ray(
                        ax,
                        ray_info,
                        order_colors[order % len(order_colors)],
                        hit_colors[order % len(hit_colors)],
                    )

        if not any(paths_dict.values()):
            print("No rays hit the target.")

    def plot_ray(self, ax, ray_info, color, hit_color):
        """Plot individual rays."""
        origin = ray_info["origin"]
        reflection_point = ray_info["reflection_point"]
        hit_location = ray_info["hit_location"]
        if hit_location is not None:
            ax.plot(
                [origin[0], hit_location[0]],
                [origin[1], hit_location[1]],
                [origin[2], hit_location[2]],
                color=color,
            )
        else:
            ax.scatter(
                reflection_point[0],
                reflection_point[1],
                reflection_point[2],
                c=hit_color,
            )
            ax.plot(
                [origin[0], reflection_point[0]],
                [origin[1], reflection_point[1]],
                [origin[2], reflection_point[2]],
                color=color,
            )

    def print_ray_info(self, ray_info):
        """Print ray information."""
        origin = ray_info["origin"]
        direction = ray_info["direction"]
        reflection_point = ray_info["reflection_point"]
        order = ray_info["order"]
        face_index = ray_info["face_index"]
        distance = ray_info["distance"]
        energy = ray_info["energy"]
        hit_location = ray_info["hit_location"]

        print(f"Ray Info (Order {order}):")
        print(f"  Origin:         {origin}")
        print(f"  Direction:      {direction}")
        print(f"  Face Index:     {face_index}")
        print(f"  Distance:       {distance}")
        print(f"  Energy:         {energy}")
        print(f"  Hit Location:   {hit_location}")
        print(
            f"  Reflection Point: {reflection_point if reflection_point is not None else 'None'}"
        )

        print("-" * 40)
