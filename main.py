import numpy as np
from mirror_image_method import MirrorImageMethod
from visualization import MeshVisualizer
from utils import Target

def main():
    mesh_file_path = "./model/simple_cube_normals_flipped.obj"
    source_point = np.array([0.123, 0.2, 0.113])
    target_face = 5
    target = Target(np.array([0.683, 0.5, 0.433]), 0.1)
    reflections_order = 10

    room = MirrorImageMethod(mesh_file_path, source_point, target, reflections_order)
    visualizer = MeshVisualizer(room, target_face)
    # room.calculatePaths():
    visualizer.plot_mesh()

    for order, paths in room.paths.items():
        print(f"\nPaths with {order} reflections:")
        for path in paths:
            travel_time = path.calculate_travel_time()
            print(f"  Travel time: {travel_time:.6f} seconds")

if __name__ == "__main__":
    main()
    