import trimesh
import numpy.linalg as lin
import numpy as np
import matplotlib.pyplot as plt

mesh = trimesh.load_mesh('./model/simple_cube_normals_flipped.obj')

FACE = 2

normals = []
for face in mesh.faces:
    v0 = mesh.vertices[face[0]]
    v1 = mesh.vertices[face[1]]
    v2 = mesh.vertices[face[2]]
    e0 = v1 - v0
    e1 = v2 - v0

    normal = lin.cross(e0,e1)
    normal = normal / lin.vector_norm(normal)
    normals.append(normal)

normals = np.array(normals)

ps = np.array([0,0,0])

def mirror_source(source, normal):
    return source - (2*np.dot(source, normal)*normal)


normal1 = normals[FACE]

mirrored_ps = mirror_source(ps, normal1)


x = mesh.vertices[:,0]
y = mesh.vertices[:,1]
z = mesh.vertices[:,2]

# Erstelle einen 3D-Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([1,1,1])


# Zeichne die Punkte
ax.scatter(x, y, z, c='black', marker='o')
ax.scatter(ps[0],ps[1],ps[2], c='b')


for index, face in enumerate(mesh.faces):
    color = 'black'
    ax.plot([mesh.vertices[face[0], 0],mesh.vertices[face[1], 0]],
            [mesh.vertices[face[0], 1],mesh.vertices[face[1], 1]],
            [mesh.vertices[face[0], 2],mesh.vertices[face[1], 2]], c=color, alpha=0.1)
    
    ax.plot([mesh.vertices[face[1], 0],mesh.vertices[face[2], 0]],
            [mesh.vertices[face[1], 1],mesh.vertices[face[2], 1]],
            [mesh.vertices[face[1], 2],mesh.vertices[face[2], 2]], c=color, alpha=0.1)

    ax.plot([mesh.vertices[face[2], 0],mesh.vertices[face[0], 0]],
            [mesh.vertices[face[2], 1],mesh.vertices[face[0], 1]],
            [mesh.vertices[face[2], 2],mesh.vertices[face[0], 2]], c=color, alpha=0.1)
    
for index, face in enumerate(mesh.faces):
    
    if index != FACE:
        continue
    color = "red"

    ax.plot([mesh.vertices[face[0], 0],mesh.vertices[face[1], 0]],
            [mesh.vertices[face[0], 1],mesh.vertices[face[1], 1]],
            [mesh.vertices[face[0], 2],mesh.vertices[face[1], 2]], c=color)
    
    ax.plot([mesh.vertices[face[1], 0],mesh.vertices[face[2], 0]],
            [mesh.vertices[face[1], 1],mesh.vertices[face[2], 1]],
            [mesh.vertices[face[1], 2],mesh.vertices[face[2], 2]], c=color)

    ax.plot([mesh.vertices[face[2], 0],mesh.vertices[face[0], 0]],
            [mesh.vertices[face[2], 1],mesh.vertices[face[0], 1]],
            [mesh.vertices[face[2], 2],mesh.vertices[face[0], 2]], c=color)


# Optional: Beschrifte die Achsen
ax.set_xlabel('X Achse')
ax.set_ylabel('Y Achse')
ax.set_zlabel('Z Achse')

# Titel des Plots
ax.set_title('3D Punkte Plot')
# Zeige nur das Grid auf der XY-Ebene


# Zeige den Plot
plt.show()