import random


labyrinthe = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 0]
]

deplacements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

entree = (0, 0)
sortie = (9, 9)

nombre_deplacements = 40

nombre_individu = 70

max_generation = 300

probabilite_croisement = 0.9

probabilite_mutation = 0.3

generation = []



def parcours(individu):
    position = entree
    chemin = [position]
    for deplacement in individu:
        ligne = position[0] + deplacements[deplacement][0]
        colonne = position[1] + deplacements[deplacement][1]
        if(ligne < 0 or ligne > 9 or colonne < 0 or colonne > 9):
            break
        if(labyrinthe[ligne][colonne] == 1):
            break
        position = (ligne, colonne)
        if(position in chemin):
            break
        chemin.append(position)
        if(position == sortie):
            break
    return chemin



def calculer_distances():
    distances = {sortie: 0}
    file = [sortie]
    while(len(file) > 0):
        case = file.pop(0)
        for d in deplacements:
            ligne = case[0] + d[0]
            colonne = case[1] + d[1]
            if(0 <= ligne <= 9 and 0 <= colonne <= 9 and labyrinthe[ligne][colonne] == 0 and (ligne, colonne) not in distances):
                distances[(ligne, colonne)] = distances[case] + 1
                file.append((ligne, colonne))
    return distances


distances_sortie = calculer_distances()


def distance_sortie(individu):
    derniere = parcours(individu)[-1]
    return distances_sortie[derniere]



def creation_individu():
    Indi = [random.randint(0, 3) for i in range(nombre_deplacements)]
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
    mini = distance_sortie(generation[0])
    for i in range(0, len(generation), 1):
        res = distance_sortie(generation[i])
        if(mini > res):
            mini = res
            x = i
    son = []
    son.append(mini)
    son.append(x)
    return son


def afficheGeneration(generation, nombreGeneration):
    res = evaluation(generation)
    print("Generation", nombreGeneration, ": meilleur individu", generation[res[1]], "distance:", res[0])



def croisement(init, individu1, individu2):
    parent1 = individu1
    parent2 = individu2
    gen1 = []
    gen2 = []

    # ---- CROISEMENT A 1 POINT : debut du parent1 + fin du parent2 (et inversement) (METHODE UTILISEE) ----
    position = random.randint(1, nombre_deplacements - 1)
    gen1 = parent1[:position] + parent2[position:]
    gen2 = parent2[:position] + parent1[position:]

    # ---- CROISEMENT A 2 POINTS : le morceau entre 2 points est echange entre les parents ----
    # point1, point2 = sorted(random.sample(range(nombre_deplacements), 2))
    # gen1 = parent1[:point1] + parent2[point1:point2 + 1] + parent1[point2 + 1:]
    # gen2 = parent2[:point1] + parent1[point1:point2 + 1] + parent2[point2 + 1:]

    # ---- CROISEMENT UNIFORME : un masque 0/1 choisit, position par position, le parent qui donne le deplacement ----
    # masque = [random.randint(0, 1) for i in range(nombre_deplacements)]
    # gen1 = [parent1[i] if masque[i] == 1 else parent2[i] for i in range(nombre_deplacements)]
    # gen2 = [parent2[i] if masque[i] == 1 else parent1[i] for i in range(nombre_deplacements)]

    init.append(gen1)
    init.append(gen2)


def mutation(individu):
    i = random.randint(0, nombre_deplacements - 1)
    individu[i] = random.choice([d for d in range(4) if d != individu[i]])
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
    scores = [distance_sortie(x) for x in generation]
    parents = []

    # ---- ROULETTE : proba proportionnelle a 1 / (distance + 1) (plus petite distance = plus de chance) (METHODE UTILISEE) ----
    poids = [1 / (s + 1) for s in scores]
    while(len(parents) < nombre_individu):
        i = random.choices(range(len(generation)), weights=poids)[0]
        parents.append(generation[i][:])

    # ---- TOURNOI : on tire 3 individus au hasard, on garde celui qui a la plus petite distance ----
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

chemin = parcours(meilleur_individu)
print('le meilleur individu est : ', meilleur_individu)
print('le meilleur score est :', meilleur_score)
print('le chemin (ligne, colonne) est :', [(l + 1, c + 1) for l, c in chemin])
print('nombre de generations :', nombre_generation)
if(meilleur_score == 0):
    print('la sortie est atteinte en', len(chemin) - 1, 'deplacements')
else:
    print('la sortie n\'est pas atteinte')