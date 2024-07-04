import numpy as np
from mirror_image_method import MirrorImageMethod
from visualization import MeshVisualizer
from utils import Ray, Target

def main():
    mesh_file_path = "./model/simple_cube_normals_flipped.obj"
    source_point = np.array([0.123, 0.2, 0.113])
    target_face = 5
    target = Target(np.array([0.683, 0.5, 0.433]), 0.1)
    reflections_order = 1

    room = MirrorImageMethod(mesh_file_path, source_point, target, reflections_order)
    visualizer = MeshVisualizer(room, source_point, reflections_order, target_face, target)

    # room.calculatePaths():
    visualizer.plot_mesh()

if __name__ == "__main__":
    main()
