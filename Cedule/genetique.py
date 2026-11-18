import random

groupe1 = ['1100', '0110', '0011']
groupe2 = ['1000', '0100', '0010', '0001']
nombre_gene = 7
nombre_individu = 20
max_generation = 30
taux_mutation = 0.2
capacite = [30, 20, 25, 40, 15, 10, 20]
capacite_maximum = sum(capacite)
intervalle = [85, 90, 70, 75]


def creation_individu():
    Indi = []
    for i in range(nombre_gene):
        if i < 2:
            x = random.choice(groupe1)
            Indi.append(x)
        else:
            x = random.choice(groupe2)
            Indi.append(x)
    return Indi


def createGeneration():
    generation = []
    for i in range(0, nombre_individu, 1):
        individu = creation_individu()
        while individu in generation:
            individu = creation_individu()
        generation.append(individu)
    return generation


def puissance(individu, capacite):
    somme = []
    for i in range(4):
        x = 0
        for j in range(7):
            x += int(individu[j][i]) * capacite[j]
        somme.append(x)
    return somme


def reser_maxi(intervalle, puiss):
    reserv = []
    for i in range(0, 4, 1):
        reserv.append(capacite_maximum - puiss[i] - intervalle[i])
    if min(reserv) < 0:
        return 0
    return min(reserv)


def croisement_point(init, individu1, individu2, position):
    parent1 = individu1
    parent2 = individu2
    gen1 = []
    gen2 = []
    for i in range(0, position, 1):
        gen1.append(parent2[i])
        gen2.append(parent1[i])
    for i in range(position, 7, 1):
        gen1.append(parent1[i])
        gen2.append(parent2[i])
    init.append(gen1)
    init.append(gen2)


def mutation(individu, position):
    if position < 2:
        individu[position] = random.choice(groupe1)
    else:
        individu[position] = random.choice(groupe2)
    return individu


def selection(generation):
    scores = []
    for individu in generation:
        scores.append(reser_maxi(intervalle, puissance(individu, capacite)))
    total = sum(scores)
    if total == 0:
        return random.choice(generation)
    r = random.uniform(0, total)
    cumul = 0
    for i in range(len(generation)):
        cumul += scores[i]
        if cumul >= r:
            return generation[i]
    return generation[-1]


def developpement_generation(generation1, position_croisement):
    nouvelle = []
    while len(nouvelle) < nombre_individu:
        parent1 = selection(generation1)
        parent2 = selection(generation1)
        croisement_point(nouvelle, parent1, parent2, position_croisement)
    for individu in nouvelle:
        if random.random() < taux_mutation:
            mutation(individu, random.randrange(nombre_gene))
    return nouvelle[:nombre_individu]


def evaluation(generation):
    x = 0
    max = -1
    son = []
    for i in range(0, len(generation), 1):
        res = reser_maxi(intervalle, puissance(generation[i], capacite))
        if max < res:
            max = res
            x = i
    son.append(max)
    son.append(x)
    return son


def afficheGeneration(generation, nombreGeneration):
    ev = evaluation(generation)
    print('Generation ', nombreGeneration, ': meilleur individu', generation[ev[1]], 'max_res:', ev[0])


random.seed(42)
nombre_generation = 1
generation = createGeneration()
afficheGeneration(generation, nombre_generation)

evaluation_generation = evaluation(generation)
meilleur_individu = generation[evaluation_generation[1]][:]
meilleur_score = evaluation_generation[0]

while nombre_generation < max_generation:
    generation = developpement_generation(generation, random.randint(1, 6))
    nombre_generation += 1
    afficheGeneration(generation, nombre_generation)

    evaluation_generation = evaluation(generation)
    if evaluation_generation[0] > meilleur_score:
        meilleur_score = evaluation_generation[0]
        meilleur_individu = generation[evaluation_generation[1]][:]

print()
print('le meilleur individu est : ', meilleur_individu)
print('les reserves par intervalle sont :', [capacite_maximum - p - d for p, d in zip(puissance(meilleur_individu, capacite), intervalle)])
print('le meilleur score est :', meilleur_score)