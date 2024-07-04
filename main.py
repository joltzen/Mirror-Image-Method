import numpy as np
from mirror_image_method import MirrorImageMethod
from visualization import MeshVisualizer
from utils import Ray, Target


def main():
    mesh_file_path = "./model/simple_cube_normals_flipped.obj"
    source_point = np.array([0.123, 0.2, 0.113])
    target_face = 5
    # Test für target ray 1
    target_center = [0.683, 0.5, 0.433]
    target_radius = 0.1
    # Test für target first reflection
    # target = [1.0, 0.54592857, 0.61392857]

    # target = [0.5, 1.0, 0.5]

    reflections_order = 1

    room = MirrorImageMethod(
        mesh_file_path, source=source_point, target=Target(target_center, target_radius), order=reflections_order
    )
    visualizer = MeshVisualizer(room, source_point, reflections_order, target_face, target=Target(target_center, target_radius))
    


    # room.calculatePaths():
    visualizer.plot_mesh()


if __name__ == "__main__":
    main()
