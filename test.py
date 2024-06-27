import numpy as np

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
    
    # Umwandeln in Grad
    theta_deg = np.degrees(theta_rad)
    
    return theta_deg

# Beispielvektoren
vector_a = np.array([1, 0, 0])
vector_b = np.array([0, 1, 0])

angle = angle_between_vectors(vector_a, vector_b)
print("Winkel zwischen den Vektoren:", angle, "Grad")
