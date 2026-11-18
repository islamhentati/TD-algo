import random

INF = float("inf")   # pas de route entre les deux villes


def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale


def generer_population(taille_population, nombre_villes):
    population = []
    for _ in range(taille_population):
        individu = list(range(nombre_villes))
        random.shuffle(individu)
        population.append(individu)
    return population


def selection(population, matrice_distances):
    """Sélection par tournoi : le meilleur de 3 individus pris au hasard."""
    candidats = random.sample(population, 3)
    return min(candidats, key=lambda x: calculer_distance_totale(x, matrice_distances))


def croisement(parent1, parent2):
    """Croisement OX : un segment du parent1, le reste dans l'ordre du parent2."""
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    enfant = [None] * n
    enfant[a:b + 1] = parent1[a:b + 1]
    reste = [ville for ville in parent2 if ville not in enfant]
    k = 0
    for i in range(n):
        if enfant[i] is None:
            enfant[i] = reste[k]
            k += 1
    return enfant


def mutation(individu, taux_mutation):
    individu = individu[:]
    if random.random() < taux_mutation:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu


def genetique(matrice_distances, taille_population, nombre_generations, taux_mutation):
    nombre_villes = len(matrice_distances)
    population = generer_population(taille_population, nombre_villes)

    meilleure_solution = min(population, key=lambda x: calculer_distance_totale(x, matrice_distances))
    meilleure_distance = calculer_distance_totale(meilleure_solution, matrice_distances)

    for _ in range(nombre_generations):
        # élitisme : on garde les 2 meilleurs
        population.sort(key=lambda x: calculer_distance_totale(x, matrice_distances))
        nouvelle_population = population[:2]

        while len(nouvelle_population) < taille_population:
            parent1 = selection(population, matrice_distances)
            parent2 = selection(population, matrice_distances)
            enfant = croisement(parent1, parent2)
            enfant = mutation(enfant, taux_mutation)
            nouvelle_population.append(enfant)

        population = nouvelle_population

        candidat = min(population, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_candidat = calculer_distance_totale(candidat, matrice_distances)
        if distance_candidat < meilleure_distance:
            meilleure_solution = candidat[:]
            meilleure_distance = distance_candidat

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

taille_population = 50
nombre_generations = 100
taux_mutation = 0.2

random.seed(42)
meilleure_solution, meilleure_distance = genetique(
    matrice_distances, taille_population, nombre_generations, taux_mutation)

print("Meilleure solution trouvée (Algorithme génétique):", meilleure_solution)
print("Distance minimale:", meilleure_distance)