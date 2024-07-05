import numpy as np
from mirror_image_method import MirrorImageMethod
from visualization import MeshVisualizer
from utils import Target


def main():
    mesh_file_path = "./model/simple_cube_normals_flipped.obj"
    source_point = np.array([0.123, 0.2, 0.113])
    target_face = 5
    target_position = Target.generate_random_coordinates()
    target = Target(target_position, 0.1)
    reflections_order = 10
    reflection_coefficient = 0.9


    room = MirrorImageMethod(mesh_file_path, source_point, target, reflections_order, reflection_coefficient=reflection_coefficient)
    visualizer = MeshVisualizer(room)

    visualizer.plot_mesh()

    for order, paths in room.paths.items():
        print(f"\nPaths with {order} reflections:")
        for path in paths:
            travel_time = path.calculate_travel_time()
            energy_loss = path.calculate_energy_loss()
            print(f"  Travel time: {travel_time:.6f} seconds")
            print(f"  Energy remaining: {energy_loss:.6f}")


if __name__ == "__main__":
    main()
    