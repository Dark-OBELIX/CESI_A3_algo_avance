from pulp import *

# Noms des villes
villes = ['A', 'B', 'C', 'D']

# Distances entre les villes (matrice symétrique)
distances = {
    ('A', 'B'): 10, ('A', 'C'): 15, ('A', 'D'): 20,
    ('B', 'C'): 35, ('B', 'D'): 25,
    ('C', 'D'): 30
}

# Compléter la matrice symétrique
for (i, j) in list(distances.keys()):
    distances[(j, i)] = distances[(i, j)]

# Créer les variables de décision
x = LpVariable.dicts('x', distances.keys(), 0, 1, LpBinary)

# Créer le problème
prob = LpProblem("TSP", LpMinimize)

# Fonction objectif
prob += lpSum(distances[i, j] * x[i, j] for i, j in distances)

# Contraintes
for k in villes:
    prob += lpSum(x[(i, k)] for i in villes if (i, k) in x) == 1
    prob += lpSum(x[(k, j)] for j in villes if (k, j) in x) == 1

# Résoudre le problème
prob.solve()
print(LpStatus[prob.status])

# Afficher la solution
for i, j in x:
    if x[i, j].varValue > 0.5:
        print(f"{i} -> {j}")

# Afficher la distance totale
print("Distance totale =", value(prob.objective))
