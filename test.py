import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Beispiel Mesh-Daten
class Mesh:
    def __init__(self):
        self.vertices = np.array([
            [1.0, 1.0, -1.0],
            [1.0, -1.0, -1.0],
            [1.0, 1.0, 1.0],
            [1.0, -1.0, 1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, -1.0],
            [-1.0, 1.0, 1.0],
            [-1.0, -1.0, 1.0]
        ])
        self.faces = np.array([
            [0, 2, 6],
            [0, 6, 4],
            [1, 5, 7],
            [1, 7, 3],
            [0, 1, 3],
            [0, 3, 2],
            [4, 6, 7],
            [4, 7, 5],
            [0, 4, 5],
            [0, 5, 1],
            [2, 3, 7],
            [2, 7, 6]
        ])

mesh = Mesh()
FACE = 3  # Beispielwert für das Face, das grün eingefärbt werden soll

# Erstelle einen 3D-Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Zeichne die Linien
for index, face in enumerate(mesh.faces):
    color = 'green' if index == FACE else 'blue'
    print(f"Index: {index}, FACE: {FACE}, Color: {color}")
    
    ax.plot([mesh.vertices[face[0], 0], mesh.vertices[face[1], 0]],
            [mesh.vertices[face[0], 1], mesh.vertices[face[1], 1]],
            [mesh.vertices[face[0], 2], mesh.vertices[face[1], 2]], c=color)
    
    ax.plot([mesh.vertices[face[1], 0], mesh.vertices[face[2], 0]],
            [mesh.vertices[face[1], 1], mesh.vertices[face[2], 1]],
            [mesh.vertices[face[1], 2], mesh.vertices[face[2], 2]], c=color)

    ax.plot([mesh.vertices[face[2], 0], mesh.vertices[face[0], 0]],
            [mesh.vertices[face[2], 1], mesh.vertices[face[0], 1]],
            [mesh.vertices[face[2], 2], mesh.vertices[face[0], 2]], c=color)

# Optional: Beschrifte die Achsen
ax.set_xlabel('X Achse')
ax.set_ylabel('Y Achse')
ax.set_zlabel('Z Achse')

# Titel des Plots
ax.set_title('3D Punkte Plot mit bedingten Linienfarben')

# Zeige die Legende
ax.legend()

# Zeige den Plot
plt.show()
