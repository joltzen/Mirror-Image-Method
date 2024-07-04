import matplotlib.pyplot as plt

# Definieren Sie die Punkte A und B
punkt_a = (1, 2)
punkt_b = (4, 5)

# Erstellen Sie den Plot
plt.figure()

# Optional: Zeichnen Sie andere Datenpunkte oder Plotelemente

# Fügen Sie die Linie von Punkt A nach Punkt B hinzu
plt.plot([punkt_a[0], punkt_b[0]], [punkt_a[1], punkt_b[1]], label='Linie von A nach B', color='red')

# Labels und Titel hinzufügen
plt.xlabel('X-Achse')
plt.ylabel('Y-Achse')
plt.title('Plot mit Linie von Punkt A nach Punkt B')
plt.legend()

# Plot anzeigen
plt.show()
