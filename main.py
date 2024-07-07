import numpy as np
from mirror_image_method import MirrorImageMethod
from visualization import MeshVisualizer
from utils import Target
import matplotlib.pyplot as plt


def main():
    # Path to the mesh file
    mesh_file_path = "./model/cube5.obj"

    # Source point of the sound
    source_point = np.array([0.123, 0.2, 0.113])

    # Target point of the sound 
    target_face = 5

    # Generate a target Object with random coordinates and radius that will be hit by the sound
    target_position = Target.generate_random_coordinates()
    target_radius = 0.5
    target = Target(target_position, target_radius)

    # Reflection order and reflection coefficient
    reflections_order = 2
    reflection_coefficient = 1.0
    
    # Number of initial rays to be generated from the source point
    initial_rays = 10000

    room = MirrorImageMethod(
        mesh_file_path,
        source_point,
        target,
        reflections_order,
        reflection_coefficient=reflection_coefficient,
        initial_rays = initial_rays
    )
    visualizer = MeshVisualizer(room)

    # Plot the mesh
    visualizer.plot_mesh()


if __name__ == "__main__":
    main()
