import numpy as np
from mesh_handler import MeshHandler
from visualization import MeshVisualizer

def main():
    mesh_file_path = './model/simple_cube_normals_flipped.obj'
    source_point = np.array([0.123, 0.2, 0.113])
    reflections_order = 2
    target_face = 8

    mesh_handler = MeshHandler(mesh_file_path)
    visualizer = MeshVisualizer(mesh_handler, source_point, reflections_order, target_face)

    visualizer.plot_mesh()

if __name__ == "__main__":
    main()
