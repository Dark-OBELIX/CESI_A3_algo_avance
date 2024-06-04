from collections import deque
import copy

def degreSommetGrapheMatrice(matrice, sommet): 
    degre = 0
    for i in range(len(matrice[sommet])): 
        degre += matrice[sommet][i] # si l'arête existe, on l'ajoute au degré
    return degre

def cycleEulerien(matrice):
    matrice = copy.deepcopy(matrice)
    n = len(matrice) 

    cycle = deque()
    stack = deque()
    cur = 0

    while(len(stack) > 0 or degreSommetGrapheMatrice(matrice, cur) != 0):
        if degreSommetGrapheMatrice(matrice, cur) == 0: # si le sommet courant n'a pas de voisin
            cycle.appendleft(cur) # ajoute le sommet courant au début du cycle
            cur = stack.pop() # revient au sommet précédent dans la pile
        else: # si le sommet courant a au moins un voisin
            for i in range(n):
                if matrice[cur][i] == 1: # si le voisin existe
                    stack.append(cur) # ajoute le sommet courant à la pile
                    matrice[cur][i] = 0 # retire l'arête de la matrice
                    matrice[i][cur] = 0 # retire l'arête dans l'autre sens
                    cur = i # le voisin devient le sommet courant
                    break # arrête la recherche des voisins

    cycle.appendleft(cur) # ajoute le dernier sommet au début du cycle
    return cycle

matrix_zone_A = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 0]]
print("### Calcul d'un cycle Eulérien du graphe de la Zone A ###")
cycle = cycleEulerien(matrix_zone_A)
for sommet in cycle: 
    print(sommet+1, "-> ", end = '') 
print(cycle[0]+1)
