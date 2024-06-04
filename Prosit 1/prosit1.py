import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time
from collections import deque
import copy

#----------------------------------------------------------#
def degreSommetGrapheMatrice(matrice, sommet): 
    degre = 0
    for i in range(len(matrice[sommet])): 
        degre += matrice[sommet][i] # si l'arête existe, on l'ajoute au degré
    return degre

def changement_representation(tab_entete, tab_succ):
    tab_temp_entete = []
    tab_temp_succ = []

    for i in range (0,len(tab_entete)-1):
        tab_temp_entete.append(i+1)
        tab_temp_succ.append([],)
        for ii in range (tab_entete[i] - 1, tab_entete[i+1] -1):
            tab_temp_succ[i].append(tab_succ[ii])
    return tab_temp_entete, tab_temp_succ

tab_entete_0 = [1,4,9,12,15]
tab_succ_0 = [2,2,3,1,1,3,4,4,1,2,4,2,2,3]

#----------------------------------------------------------#
def AFFICHAGE_graphe(head_zone_A, succ_zone_A):

    A = nx.DiGraph()

    A.add_nodes_from(head_zone_A)

    for i, adj_list in enumerate(succ_zone_A):
        for adj_node in adj_list:
            A.add_edge(head_zone_A[i], adj_node)

    nx.draw(A, with_labels=True, node_color='red', node_size=1500, font_size=10)
    plt.show()

def matrice_adjacence(head_zone, Adj_zone):
    # Initialisation de la matrice d'adjacence avec des zéros
    matrice = [[0] * len(head_zone) for _ in range(len(head_zone))]
    
    # Parcours des zones et de leurs adjacences pour mettre à jour la matrice
    for i, zone in enumerate(head_zone):
        index_zone = head_zone.index(zone)
        for adj_zone in Adj_zone[i]:
            index_adj_zone = head_zone.index(adj_zone)
            # Marquer l'adjacence dans la matrice en mettant 1
            matrice[index_zone][index_adj_zone] = 1
    
    return matrice

def affichage_matrice(matrice):
    for row in matrice:
        print(row)

def degre_graphe(matrice_adjacence):
    degres = []
    for i in range(len(matrice_adjacence)):
        degre = sum(matrice_adjacence[i])
        degres.append(degre)
    return degres

def existeCycleEulerien(matrice):
    for sommet in range (len(matrice)):
        degre = 0
        a = 0 
        for i in range (len(matrice)):
            degre += matrice[sommet][i]
        if degre % 2 != 0:
            a = a + 1
    if a == 2 or a == 0:
        return True
    else:
        return False

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
#----------------------------------------------------------#

def main():

    start_time = time.time()

    head_zone_A = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    Adj_zone_A = [["B", "J"], ["A", "C"], ["B", "D"], ["C", "E", "I", "G"], ["D", "F"], ["E", "G"],
                   ["D", "F", "H", "I"], ["G", "I"], ["D", "G", "J","H"], ["A", "I"]]

    matrix = matrice_adjacence(head_zone_A, Adj_zone_A)
    print("Matrice d'adjacence:")
    affichage_matrice(matrix)
    print("")

    degres = degre_graphe(matrix)
    print("Degrés des zones:", degres)
    print("")

    if (existeCycleEulerien(matrix)):
        print ("Le graphe est eulérien")
        print(cycleEulerien(matrix))
    else:
        print ("Le graphe n'est pas eulérien")
    

    end_time = time.time()
    print("Temps d'exécution:", end_time - start_time, "secondes")

if __name__ == "__main__":
    main()
