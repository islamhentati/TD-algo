import random


def calculer_cout_total(solut, couts):
    cout = 0
    for i in range(len(solut)):
        for j in range(len(solut[0])):
            cout += solut[i][j] * couts[i][j]
    return cout


def stock_respecte(solut, stocks):
    for i in range(len(solut)):
        if sum(solut[i]) > stocks[i]:
            return False
    return True


def calculer_fitness(solut, couts, stocks, cout_max):
    if not stock_respecte(solut, stocks):
        return 0
    return cout_max - calculer_cout_total(solut, couts)


def generer_individu(demandes, nbr_depots):
    solut = [[0] * len(demandes) for i in range(nbr_depots)]
    for j in range(len(demandes)):
        for c in range(demandes[j]):
            solut[random.randrange(nbr_depots)][j] += 1
    return solut


def generer_population(taille_pop, demandes, nbr_depots):
    population = []
    for i in range(taille_pop):
        population.append(generer_individu(demandes, nbr_depots))
    return population


def selection_roulette(population, fitness):
    total = sum(fitness)
    if total == 0:
        return random.choice(population)
    r = random.uniform(0, total)
    cumul = 0
    for i in range(len(population)):
        cumul += fitness[i]
        if cumul >= r:
            return population[i]
    return population[-1]


def croisement(parent1, parent2, taux_croisement):
    if random.random() < taux_croisement:
        point = random.randint(1, len(parent1[0]) - 1)
        enfant1 = [parent1[i][:point] + parent2[i][point:] for i in range(len(parent1))]
        enfant2 = [parent2[i][:point] + parent1[i][point:] for i in range(len(parent1))]
        return enfant1, enfant2
    return [ligne[:] for ligne in parent1], [ligne[:] for ligne in parent2]


def mutation(individu, taux_mutation):
    individu = [ligne[:] for ligne in individu]
    if random.random() < taux_mutation:
        a, b = random.sample(range(len(individu)), 2)
        j, k = random.sample(range(len(individu[0])), 2)
        if individu[a][j] > 0 and individu[b][k] > 0:
            individu[a][j] -= 1
            individu[b][j] += 1
            individu[b][k] -= 1
            individu[a][k] += 1
    return individu


def genetic_algorithm(couts, stocks, demandes, taille_pop, nbr_generations, taux_croisement, taux_mutation):
    cout_max = sum(demandes[j] * max(couts[i][j] for i in range(len(couts))) for j in range(len(demandes)))
    population = generer_population(taille_pop, demandes, len(stocks))

    meilleur_solut = None
    meilleur_fitness = -1

    for g in range(nbr_generations):
        fitness = [calculer_fitness(x, couts, stocks, cout_max) for x in population]

        for i in range(len(population)):
            if fitness[i] > meilleur_fitness:
                meilleur_solut = [ligne[:] for ligne in population[i]]
                meilleur_fitness = fitness[i]

        nouvelle_population = [[ligne[:] for ligne in meilleur_solut]]
        while len(nouvelle_population) < taille_pop:
            parent1 = selection_roulette(population, fitness)
            parent2 = selection_roulette(population, fitness)
            enfant1, enfant2 = croisement(parent1, parent2, taux_croisement)
            nouvelle_population.append(mutation(enfant1, taux_mutation))
            nouvelle_population.append(mutation(enfant2, taux_mutation))

        population = nouvelle_population[:taille_pop]

    for x in population:
        f = calculer_fitness(x, couts, stocks, cout_max)
        if f > meilleur_fitness:
            meilleur_solut = [ligne[:] for ligne in x]
            meilleur_fitness = f

    return meilleur_solut, calculer_cout_total(meilleur_solut, couts)


couts = [
    [5, 3, 4],
    [6, 7, 2]
]
stocks = [8, 9]
demandes = [4, 5, 8]

taille_pop = 50
nbr_generations = 100
taux_croisement = 0.8
taux_mutation = 0.3

random.seed(42)
meilleur_solut, meilleur_cout = genetic_algorithm(couts, stocks, demandes, taille_pop,
                                                  nbr_generations, taux_croisement, taux_mutation)

print("Meilleure solution trouvée (Algorithme génétique):", meilleur_solut)
print("Containers envoyes par depot:", [sum(ligne) for ligne in meilleur_solut])
print("Containers recus par magasin:", [sum(meilleur_solut[i][j] for i in range(len(stocks))) for j in range(len(demandes))])
print("Cout total minimal:", meilleur_cout)