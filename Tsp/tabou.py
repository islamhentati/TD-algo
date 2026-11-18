import random
from collections import deque

INF = float("inf")   # pas de route entre les deux villes


def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale


def generer_voisins(solution):
    voisins = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins


def tabu_search(matrice_distances, nombre_iterations, taille_tabu):
    nombre_villes = len(matrice_distances)
    solution_actuelle = list(range(nombre_villes))

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)

    tabu_list = deque(maxlen=taille_tabu)

    for _ in range(nombre_iterations):
        voisins = generer_voisins(solution_actuelle)
        voisins = [voisin for voisin in voisins if voisin not in tabu_list]

        if not voisins:
            break

        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

        tabu_list.append(solution_actuelle)

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance


# Distances entre les 7 villes (matrice symétrique, la ville 1 est à l'indice 0)
matrice_distances = [
    [  0,  12,  10, INF, INF, INF,  12],
    [ 12,   0,   8,  12, INF, INF, INF],
    [ 10,   8,   0,   3,   9, INF, INF],
    [INF,  12,   3,   0,  11,   7, INF],
    [INF, INF,   9,  11,   0,  10,   6],
    [INF, INF, INF,   7,  10,   0,   9],
    [ 12, INF, INF, INF,   6,   9,   0]
]

nombre_iterations = 50
taille_tabu = 10

meilleure_solution, meilleure_distance = tabu_search(matrice_distances, nombre_iterations, taille_tabu)

print("Meilleure solution trouvée (Tabu Search):", meilleure_solution)
print("Distance minimale:", meilleure_distance)