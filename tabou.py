import sys
import random
from collections import deque
from tqdm import tqdm
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg


def generate_random_distance_matrix(num_villes, min_distance, max_distance):

    matrix = [[0 if i == j else random.randint(min_distance, max_distance) for j in range(num_villes)] for i in range(num_villes)]
    for i in range(num_villes):
        for j in range(i + 1, num_villes):
            matrix[j][i] = matrix[i][j]
    return matrix



def valeur_contenu(solution):
    """Calculer la distance totale pour une solution donnée"""
    return sum(distances[solution[i-1]][solution[i]] for i in range(num_villes))

def voisinage(solution):
    """Générer tous les voisins d'une solution en permutant deux villes"""
    voisins = []
    for i in range(num_villes):
        for j in range(i + 1, num_villes):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins

def recherche_tabou_traject(solution_initiale, taille_tabou, iter_max):
    """
    Algorithme de recherche tabou pour résoudre le TSP.
    """
    nb_iter = 0
    liste_tabou = deque((), maxlen=taille_tabou)

    # Variables solutions pour la recherche du voisin optimal non tabou
    solution_courante = solution_initiale
    meilleure = solution_initiale
    meilleure_globale = solution_initiale

    # Variables valeurs pour la recherche du voisin optimal non tabou
    valeur_meilleure = valeur_contenu(solution_initiale)
    valeur_meilleure_globale = valeur_meilleure
    
    # Liste des solutions courantes et des meilleures trouvées, pour afficher la trajectoire
    courantes = deque()
    meilleures_courantes = deque()
    
    for _ in tqdm(range(iter_max), desc="Recherche Tabou"):
        nb_iter += 1
        valeur_meilleure = float('inf')
        
        # On parcourt tous les voisins de la solution courante
        for voisin in voisinage(solution_courante):
            valeur_voisin = valeur_contenu(voisin)
            if valeur_voisin < valeur_meilleure and voisin not in liste_tabou:
                valeur_meilleure = valeur_voisin
                meilleure = voisin

        # On met à jour la meilleure solution rencontrée depuis le début
        if valeur_meilleure < valeur_meilleure_globale:
            meilleure_globale = meilleure
            valeur_meilleure_globale = valeur_meilleure
            nb_iter = 0
        
        meilleures_courantes.append(valeur_meilleure_globale)
        courantes.append(valeur_contenu(solution_courante))
        
        # On passe au meilleur voisin non tabou trouvé
        solution_courante = meilleure
        
        # On met à jour la liste tabou
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
        self.plot_widget.plot(list(courants), pen='b', name='Solution courante')
        self.plot_widget.plot(list(meilleurs_courants), pen='r', name='Meilleure solution')

if __name__ == "__main__":

    """
    distances = [
    [0, 29, 20, 21, 17, 30, 10, 25, 11, 15],
    [29, 0, 15, 17, 28, 12, 22, 27, 16, 18],
    [20, 15, 0, 28, 22, 13, 26, 30, 25, 19],
    [21, 17, 28, 0, 19, 10, 21, 24, 18, 20],
    [17, 28, 22, 19, 0, 15, 14, 23, 17, 16],
    [30, 12, 13, 10, 15, 0, 20, 18, 12, 14],
    [10, 22, 26, 21, 14, 20, 0, 19, 11, 13],
    [25, 27, 30, 24, 23, 18, 19, 0, 16, 17],
    [11, 16, 25, 18, 17, 12, 11, 16, 0, 14],
    [15, 18, 19, 20, 16, 14, 13, 17, 14, 0]
    ]    """


    
    distances = generate_random_distance_matrix(10,50,100)

    num_villes = len(distances)

    # Initialisation de la solution avec un circuit aléatoire
    solution_initiale = random.sample(range(num_villes), num_villes)
    iter_max = 150
    taille_tabou = 7

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
