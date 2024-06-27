import trimesh
import numpy.linalg as lin
import numpy as np
import matplotlib.pyplot as plt

mesh = trimesh.load_mesh('./model/simple_cube_normals_flipped.obj')

FACE = 7

def calculate_normal(face):
    v0 = mesh.vertices[face[0]]
    v1 = mesh.vertices[face[1]]
    v2 = mesh.vertices[face[2]]
    e0 = v1 - v0
    e1 = v2 - v0

    normal = lin.cross(e0,e1)
    normal = normal / lin.vector_norm(normal)

    return normal    

ps = np.array([0.123,0.2,0.113])

def mirror_source(source, face):
    #bestimmen von zentrum des Faces
    centroid = centroid_of_face(face)

    #r berechnet
    r = centroid - source

    #Normal bestimmen
    normal = calculate_normal(face)

    #Orthogonale Projektion auf das Face
    orthogonal =  (np.dot(r, normal) * np.dot(normal, normal) * normal)
    
    return 2*orthogonal + source

def centroid_of_face(face):
    v0 = mesh.vertices[face[0]]
    v1 = mesh.vertices[face[1]]
    v2 = mesh.vertices[face[2]]

    return np.mean([v0, v1,v2], axis=0)

def angle_between_vectors(a, b):
    """
    Berechnet den Winkel zwischen zwei Vektoren in Grad.
    """
    # Skalarprodukt der Vektoren
    dot_product = np.dot(a, b)
    
    # Längen der Vektoren
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    # Kosinus des Winkels
    cos_theta = dot_product / (norm_a * norm_b)
    
    # Winkel in Radiant
    theta_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    
    
    return theta_rad

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
ax.scatter(0,0,0, c="black")


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
    
    mirrored_ps = mirror_source(ps, face)
    ax.scatter(mirrored_ps[0],mirrored_ps[1],mirrored_ps[2], c="pink")



    
    
for index, face in enumerate(mesh.faces):

    if index != FACE:
        continue
    color = "red"

    center = centroid_of_face(face)


    r = center - ps
    #Verbindung Source zum Mittelpunkt des Dreiecks    
    ax.quiver(ps[0],ps[1],ps[2], r[0],r[1],r[2], color="green")

    normal = calculate_normal(face)
    ax.quiver(center[0],center[1],center[2], normal[0],normal[1],normal[2], color="red", alpha=0.2)

    orthogonal =  (np.dot(r, normal) * np.dot(normal, normal) * normal)

    mirrored_source =  mirror_source(ps, face)
    ax.quiver(ps[0],ps[1],ps[2], orthogonal[0],orthogonal[1],orthogonal[2], color="yellow")
    ax.scatter(mirrored_source[0], mirrored_source[1],mirrored_source[2], c="blue")

    #ax.plot([orthogonal[0], ps[0]],[orthogonal[1], ps[1]],[orthogonal[2], ps[2]], c="yellow")
    ax.scatter(center[0],center[1],center[2], c="red")

    ax.plot([mesh.vertices[face[0], 0],mesh.vertices[face[1], 0]],
            [mesh.vertices[face[0], 1],mesh.vertices[face[1], 1]],
            [mesh.vertices[face[0], 2],mesh.vertices[face[1], 2]], c=color)
    
    ax.plot([mesh.vertices[face[1], 0],mesh.vertices[face[2], 0]],
            [mesh.vertices[face[1], 1],mesh.vertices[face[2], 1]],
            [mesh.vertices[face[1], 2],mesh.vertices[face[2], 2]], c=color)

    ax.plot([mesh.vertices[face[2], 0],mesh.vertices[face[0], 0]],
            [mesh.vertices[face[2], 1],mesh.vertices[face[0], 1]],
            [mesh.vertices[face[2], 2],mesh.vertices[face[0], 2]], c=color)
    
    mirrored_ps = mirror_source(ps, face)
    ax.scatter(mirrored_ps[0],mirrored_ps[1],mirrored_ps[2], c="blue")




# Optional: Beschrifte die Achsen
# ax.set_xlabel('X Achse')
# ax.set_ylabel('Y Achse')
# ax.set_zlabel('Z Achse')
ax.set_axis_off()
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
# Titel des Plots
ax.set_title('3D Punkte Plot')
# Zeige nur das Grid auf der XY-Ebene

# Zeige den Plot
plt.show()