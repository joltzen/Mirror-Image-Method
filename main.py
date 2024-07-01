import numpy as np
from mirror_image_method import MirrorImageMethod
from visualization import MeshVisualizer
from ray import Ray


def main():
    mesh_file_path = "./model/simple_cube_normals_flipped.obj"
    source_point = np.array([0.123, 0.2, 0.113])
    target = [0, 0.5, 0]
    reflections_order = 1
    target_face = 5

    room = MirrorImageMethod(
        mesh_file_path, source=source_point, target=target, order=reflections_order
    )
    visualizer = MeshVisualizer(room, source_point, reflections_order, target_face)

    # room.calculatePaths()
    visualizer.plot_mesh()


if __name__ == "__main__":
    main()
