import sys
import random
from collections import deque
from tqdm import tqdm
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
from functools import lru_cache

def generate_random_distance_matrix(num_villes, min_distance, max_distance):
    matrix = [[0 if i == j else random.randint(min_distance, max_distance) for j in range(num_villes)] for i in range(num_villes)]
    for i in range(num_villes):
        for j in range(i + 1, num_villes):
            matrix[j][i] = matrix[i][j]
    return matrix

@lru_cache(maxsize=None)
def valeur_contenu(solution):
    return sum(distances[solution[i-1]][solution[i]] for i in range(num_villes))

@lru_cache(maxsize=None)
def voisinage(solution):
    voisins = []
    solution = list(solution)
    for i in range(num_villes):
        for j in range(i + 1, num_villes):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(tuple(voisin))
    return voisins

def recherche_tabou_traject(solution_initiale, taille_tabou, iter_max):

    nb_iter = 0
    liste_tabou = deque((), maxlen=taille_tabou)

    solution_courante = tuple(solution_initiale)
    meilleure = solution_courante
    meilleure_globale = solution_courante

    valeur_meilleure = valeur_contenu(solution_courante)
    valeur_meilleure_globale = valeur_meilleure
    
    courantes = deque()
    meilleures_courantes = deque()
    
    for _ in tqdm(range(iter_max), desc="Recherche Tabou"):
        nb_iter += 1
        valeur_meilleure = float('inf')
        
        for voisin in voisinage(solution_courante):
            valeur_voisin = valeur_contenu(voisin)
            if valeur_voisin < valeur_meilleure and voisin not in liste_tabou:
                valeur_meilleure = valeur_voisin
                meilleure = voisin

        if valeur_meilleure < valeur_meilleure_globale:
            meilleure_globale = meilleure
            valeur_meilleure_globale = valeur_meilleure
            nb_iter = 0
        
        meilleures_courantes.append(valeur_meilleure_globale)
        courantes.append(valeur_contenu(solution_courante))
        
        solution_courante = meilleure
        
        liste_tabou.append(solution_courante)

    return meilleure_globale, courantes, meilleures_courantes

class TSPWindow(QMainWindow):
    def __init__(self, courants, meilleurs_courants):
        super().__init__()
        self.setWindowTitle("Recherche Tabou pour le TSP")
        
        # Configuration de la fenêtre principale
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)
        
        # Initialisation de pyqtgraph
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        
        self.plot_widget.setLabel('left', 'Distance')
        self.plot_widget.setLabel('bottom', 'Nombre d\'itérations')
        
        # Tracer les données
        self.plot_widget.plot(list(courants), pen='y', name='Solution courante')
        self.plot_widget.plot(list(meilleurs_courants), pen='w', name='Meilleure solution')

if __name__ == "__main__":
    distances = generate_random_distance_matrix(20,20,100)
    num_villes = len(distances)

    # Initialisation de la solution avec un circuit aléatoire
    solution_initiale = random.sample(range(num_villes), num_villes)
    iter_max = 150
    taille_tabou = 30

    # Chronométrer l'exécution
    start_time = time.time()
    sol, courants, meilleurs_courants = recherche_tabou_traject(solution_initiale, taille_tabou, iter_max)
    end_time = time.time()

    # Afficher le temps d'exécution
    print(f"Temps d'exécution: {end_time - start_time:.2f} secondes")

    # Exécution de l'application PyQt5
    app = QApplication(sys.argv)
    main_win = TSPWindow(courants, meilleurs_courants)
    main_win.show()
    sys.exit(app.exec_())
