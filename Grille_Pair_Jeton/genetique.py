import math
import random

n = 5
k = 10
nombre_cases = n * n
nombre_individu = 70
max_generation = 300
probabilite_croisement = 0.9
probabilite_mutation = 0.3
generation = []


taille_espace = math.comb(nombre_cases, k)


def jetons_ligne(individu, i):
    return sum(individu[i * n + j] for j in range(n))


def jetons_colonne(individu, j):
    return sum(individu[i * n + j] for i in range(n))


def lignes_colonnes_impaires(individu):
    impaires = 0
    for i in range(n):
        if(jetons_ligne(individu, i) % 2 == 1):
            impaires += 1
        if(jetons_colonne(individu, i) % 2 == 1):
            impaires += 1
    return impaires


def reparer(individu):
    pris = [i for i in range(nombre_cases) if individu[i] == 1]
    vides = [i for i in range(nombre_cases) if individu[i] == 0]
    while(len(pris) > k):
        i = random.choice(pris)
        pris.remove(i)
        individu[i] = 0
    while(len(pris) < k):
        i = random.choice(vides)
        vides.remove(i)
        individu[i] = 1
        pris.append(i)
    return individu


def creation_individu():
    Indi = [0] * nombre_cases
    for i in random.sample(range(nombre_cases), k):
        Indi[i] = 1
    return Indi


def createGeneration():
    generation = []
    for i in range(0, nombre_individu, 1):
        individu = creation_individu()
        while(individu in generation):
            individu = creation_individu()
        generation.append(individu)
    return generation


def evaluation(generation):
    x = 0
    mini = lignes_colonnes_impaires(generation[0])
    for i in range(0, len(generation), 1):
        res = lignes_colonnes_impaires(generation[i])
        if(mini > res):
            mini = res
            x = i
    son = []
    son.append(mini)
    son.append(x)
    return son


def afficheGeneration(generation, nombreGeneration):
    res = evaluation(generation)
    print("Generation", nombreGeneration, ": meilleur individu", generation[res[1]], "lignes/colonnes impaires:", res[0])


def afficheGrille(individu):
    for i in range(n):
        print(' '.join('X' if individu[i * n + j] == 1 else '.' for j in range(n)),
              '  jetons:', jetons_ligne(individu, i))
    print(' '.join(str(jetons_colonne(individu, j)) for j in range(n)), '  <- jetons par colonne')


def croisement(init, individu1, individu2):
    parent1 = individu1
    parent2 = individu2
    gen1 = []
    gen2 = []

    # ---- CROISEMENT A 1 POINT : debut du parent1 + fin du parent2 (et inversement) (METHODE UTILISEE) ----
    position = random.randint(1, nombre_cases - 1)
    gen1 = parent1[:position] + parent2[position:]
    gen2 = parent2[:position] + parent1[position:]

    # ---- CROISEMENT A 2 POINTS : le morceau entre 2 points est echange entre les parents ----
    # point1, point2 = sorted(random.sample(range(nombre_cases), 2))
    # gen1 = parent1[:point1] + parent2[point1:point2 + 1] + parent1[point2 + 1:]
    # gen2 = parent2[:point1] + parent1[point1:point2 + 1] + parent2[point2 + 1:]

    # ---- CROISEMENT UNIFORME : un masque 0/1 choisit, position par position, le parent qui donne la case ----
    # masque = [random.randint(0, 1) for i in range(nombre_cases)]
    # gen1 = [parent1[i] if masque[i] == 1 else parent2[i] for i in range(nombre_cases)]
    # gen2 = [parent2[i] if masque[i] == 1 else parent1[i] for i in range(nombre_cases)]

    init.append(reparer(gen1))
    init.append(reparer(gen2))


def mutation(individu):
    i = random.choice([c for c in range(nombre_cases) if individu[c] == 1])
    j = random.choice([c for c in range(nombre_cases) if individu[c] == 0])
    individu[i] = 0
    individu[j] = 1
    return individu


def developpement_generation(parents):
    enfants = []
    for i in range(0, nombre_individu - 1, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        if(random.random() < probabilite_croisement):
            croisement(enfants, parent1, parent2)
        else:
            enfants.append(parent1[:])
            enfants.append(parent2[:])
    for enfant in enfants:
        if(random.random() < probabilite_mutation):
            mutation(enfant)
    return enfants


def selection(generation):
    scores = [lignes_colonnes_impaires(x) for x in generation]
    parents = []

    # ---- ROULETTE : proba proportionnelle a 1 / (score + 1) (plus petit score = plus de chance) (METHODE UTILISEE) ----
    poids = [1 / (s + 1) for s in scores]
    while(len(parents) < nombre_individu):
        i = random.choices(range(len(generation)), weights=poids)[0]
        parents.append(generation[i][:])

    # ---- TOURNOI : on tire 3 individus au hasard, on garde celui qui a le plus petit score ----
    # while(len(parents) < nombre_individu):
    #     candidats = random.sample(range(len(generation)), 3)
    #     meilleur = min(candidats, key=lambda i: scores[i])
    #     parents.append(generation[meilleur][:])

    # ---- RANG : on classe du pire (rang 1) au meilleur (rang N), proba proportionnelle au rang ----
    # indices = sorted(range(len(generation)), key=lambda i: scores[i], reverse=True)
    # rangs = list(range(1, len(generation) + 1))
    # while(len(parents) < nombre_individu):
    #     i = random.choices(indices, weights=rangs)[0]
    #     parents.append(generation[i][:])

    # ---- ELITISTE : seuls les meilleurs (la moitie) peuvent devenir parents ----
    # indices = sorted(range(len(generation)), key=lambda i: scores[i])
    # meilleurs = indices[:nombre_individu // 2]
    # while(len(parents) < nombre_individu):
    #     i = random.choice(meilleurs)
    #     parents.append(generation[i][:])

    return parents




nombre_generation = 0
generation = createGeneration()
resultat = evaluation(generation)
meilleur_score = resultat[0]
meilleur_individu = generation[resultat[1]][:]

while(nombre_generation < max_generation and meilleur_score > 0):
    parents = selection(generation)
    generation = developpement_generation(parents)
    resultat = evaluation(generation)
    if(resultat[0] < meilleur_score):
        meilleur_score = resultat[0]
        meilleur_individu = generation[resultat[1]][:]
    generation[0] = meilleur_individu[:]
    nombre_generation += 1
    if(nombre_generation % 20 == 0):
        afficheGeneration(generation, nombre_generation)

print('le meilleur individu est : ', meilleur_individu)
print('le meilleur score est :', meilleur_score)
print('nombre de generations :', nombre_generation)
afficheGrille(meilleur_individu)
if(meilleur_score == 0):
    print('solution faisable : chaque ligne et chaque colonne a un nombre pair de jetons')
else:
    print('solution non faisable')