import trimesh
import numpy.linalg as lin
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider
import ipywidgets as widgets

# Lade das Mesh
mesh = trimesh.load_mesh('./model/simple_cube_normals_flipped.obj')

FACE = 2

def calculate_normal(face):
    v0 = mesh.vertices[face[0]]
    v1 = mesh.vertices[face[1]]
    v2 = mesh.vertices[face[2]]
    e0 = v1 - v0
    e1 = v2 - v0

    normal = lin.cross(e0, e1)
    normal = normal / lin.norm(normal)

    return normal

def mirror_source(source, face):
    # Bestimmen von Zentrum des Faces
    p = centroid_of_face(face)
    normal = calculate_normal(face)
    # r berechnet
    r = p - source
    # Winkel zwischen r und normale des faces
    alpha = angle_between_vectors(p, normal)
    # Spiegelpunkt bestimmen
    I = (2 * normal * lin.norm(r) * np.cos(alpha)) - source
    return I

def centroid_of_face(face):
    v0 = mesh.vertices[face[0]]
    v1 = mesh.vertices[face[1]]
    v2 = mesh.vertices[face[2]]
    return np.mean([v0, v1, v2], axis=0)

def angle_between_vectors(a, b):
    """
    Berechnet den Winkel zwischen zwei Vektoren in Grad.
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    cos_theta = dot_product / (norm_a * norm_b)
    theta_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return theta_rad

def update_plot(ps_x=0.5, ps_y=0.25, ps_z=0.3):
    ps = np.array([ps_x, ps_y, ps_z])

    x = mesh.vertices[:, 0]
    y = mesh.vertices[:, 1]
    z = mesh.vertices[:, 2]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])

    ax.scatter(x, y, z, c='black', marker='o')
    ax.scatter(ps[0], ps[1], ps[2], c='b')
    ax.scatter(0, 0, 0, c="black")

    for index, face in enumerate(mesh.faces):
        color = 'black'
        ax.plot([mesh.vertices[face[0], 0], mesh.vertices[face[1], 0]],
                [mesh.vertices[face[0], 1], mesh.vertices[face[1], 1]],
                [mesh.vertices[face[0], 2], mesh.vertices[face[1], 2]], c=color, alpha=0.1)

        ax.plot([mesh.vertices[face[1], 0], mesh.vertices[face[2], 0]],
                [mesh.vertices[face[1], 1], mesh.vertices[face[2], 1]],
                [mesh.vertices[face[1], 2], mesh.vertices[face[2], 2]], c=color, alpha=0.1)

        ax.plot([mesh.vertices[face[2], 0], mesh.vertices[face[0], 0]],
                [mesh.vertices[face[2], 1], mesh.vertices[face[0], 1]],
                [mesh.vertices[face[2], 2], mesh.vertices[face[0], 2]], c=color, alpha=0.1)

    for index, face in enumerate(mesh.faces):
        if index != FACE:
            continue
        color = "red"
        center = centroid_of_face(face)

        r = center - ps
        ax.quiver(ps[0], ps[1], ps[2], r[0], r[1], r[2], color="green")

        normal = calculate_normal(face)
        ax.quiver(center[0], center[1], center[2], normal[0], normal[1], normal[2], color="red", alpha=0.2)

        orthogonal = 2 * (np.dot(r, normal) * np.dot(normal, normal) * normal)

        mirrored_source = (orthogonal) + ps
        ax.quiver(ps[0], ps[1], ps[2], orthogonal[0], orthogonal[1], orthogonal[2], color="yellow")
        ax.scatter(mirrored_source[0], mirrored_source[1], mirrored_source[2], c="blue")

        ax.scatter(center[0], center[1], center[2], c="red")

        ax.plot([mesh.vertices[face[0], 0], mesh.vertices[face[1], 0]],
                [mesh.vertices[face[0], 1], mesh.vertices[face[1], 1]],
                [mesh.vertices[face[0], 2], mesh.vertices[face[1], 2]], c=color)

        ax.plot([mesh.vertices[face[1], 0], mesh.vertices[face[2], 0]],
                [mesh.vertices[face[1], 1], mesh.vertices[face[2], 1]],
                [mesh.vertices[face[1], 2], mesh.vertices[face[2], 2]], c=color)

        ax.plot([mesh.vertices[face[2], 0], mesh.vertices[face[0], 0]],
                [mesh.vertices[face[2], 1], mesh.vertices[face[0], 1]],
                [mesh.vertices[face[2], 2], mesh.vertices[face[0], 2]], c=color)

    ax.set_axis_off()
    ax.set_title('3D Punkte Plot')
    plt.show()

# Verwenden von ipywidgets zur Erstellung interaktiver Slider
interact(update_plot, 
         ps_x=FloatSlider(min=-1.0, max=1.0, step=0.01, value=0.5),
         ps_y=FloatSlider(min=-1.0, max=1.0, step=0.01, value=0.25),
         ps_z=FloatSlider(min=-1.0, max=1.0, step=0.01, value=0.3))
