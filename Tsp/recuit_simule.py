import math
import random

INF = float("inf")   # pas de route entre les deux villes


def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale


def generer_voisin(solution):
    voisin = solution[:]
    i, j = random.sample(range(len(voisin)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin


def recuit_simule(matrice_distances, temperature_initiale, temperature_finale,
                        alpha, iterations_par_palier):
    nombre_villes = len(matrice_distances)
    solution_actuelle = list(range(nombre_villes))
    distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle

    temperature = temperature_initiale

    while temperature > temperature_finale:
        for _ in range(iterations_par_palier):
            voisin = generer_voisin(solution_actuelle)
            distance_voisin = calculer_distance_totale(voisin, matrice_distances)

            if distance_voisin == INF:      # route inexistante : on ignore
                continue

            delta = distance_voisin - distance_actuelle

            # meilleur : on accepte, sinon on accepte avec la probabilité exp(-delta/T)
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                solution_actuelle = voisin
                distance_actuelle = distance_voisin

                if distance_actuelle < meilleure_distance:
                    meilleure_solution = solution_actuelle[:]
                    meilleure_distance = distance_actuelle

        temperature *= alpha                # refroidissement

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

temperature_initiale = 100
temperature_finale = 0.01
alpha = 0.95
iterations_par_palier = 50

random.seed(42)
meilleure_solution, meilleure_distance = recuit_simule(
    matrice_distances, temperature_initiale, temperature_finale, alpha, iterations_par_palier)

print("Meilleure solution trouvée (Recuit simulé):", meilleure_solution)
print("Distance minimale:", meilleure_distance)