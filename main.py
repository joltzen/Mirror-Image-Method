import numpy as np
from mirror_image_method import MirrorImageMethod
from visualization import MeshVisualizer
from utils import Target
import matplotlib.pyplot as plt


def main():
    mesh_file_path = "./model/cube5.obj"
    source_point = np.array([0.123, 0.2, 0.113])
    target_face = 5
    target_position = Target.generate_random_coordinates()
    target = Target(target_position, 0.5)
    reflections_order = 2
    reflection_coefficient = 1.0

    room = MirrorImageMethod(
        mesh_file_path,
        source_point,
        target,
        reflections_order,
        reflection_coefficient=reflection_coefficient,
    )
    visualizer = MeshVisualizer(room)

    visualizer.plot_mesh()

    early_energy = []
    early_time = []
    direct_energy = []
    direct_time = []

    for order, paths in room.paths.items():
        print(f"\nPaths with {order} reflections: {len(paths)}")
        for path in paths:
            if order == 0:
                direct_time.append(path.calculate_total_travel_time())
                direct_energy.append(path.calculate_energy_loss_of_all())
                continue
            early_time.append(path.calculate_total_travel_time())
            early_energy.append(path.calculate_energy_loss_of_all())

    plt.figure()
    plt.stem(
        direct_time,
        direct_energy,
        linefmt="b-",
        markerfmt="bo",
        basefmt="k-",
        label="Direct Path",
    )
    plt.stem(
        early_time,
        early_energy,
        linefmt="r-",
        markerfmt="ro",
        basefmt="k-",
        label="Early Reflections",
    )
    plt.xlabel("Time")
    plt.ylabel("Energy")
    plt.title("Room Impulse Response")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    main()
