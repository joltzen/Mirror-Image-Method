import numpy as np
from mirror_image_method import MirrorImageMethod
from visualization import MeshVisualizer
from utils import Ray, Target


def main():
    mesh_file_path = "./model/simple_cube_normals_flipped.obj"
    source_point = np.array([0.123, 0.2, 0.113])
    # Test für target ray 1
    target = Target([0.683, 0.5, 0.433], 0.1)
    order = 1

    room = MirrorImageMethod(mesh_file_path, source_point, target, order)
    room.simulate(5)

    visualizer = MeshVisualizer(room)

    visualizer.plot_mirrored_sources()
    visualizer.plot_vertices()
    visualizer.plot_faces()
    visualizer.plot_target()
    visualizer.show()


if __name__ == "__main__":
    main()
