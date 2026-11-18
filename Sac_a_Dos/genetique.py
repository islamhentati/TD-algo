import random


def calculer_poids_total(solut, poids):
    pt = 0
    for i in range(len(solut)):
        if solut[i] == 1:
            pt += poids[i]
    return pt


def calculer_valeur_totale(solut, valeurs):
    vt = 0
    for i in range(len(solut)):
        if solut[i] == 1:
            vt += valeurs[i]
    return vt


def evaluer(solut, valeurs, poids, capacite):
    if calculer_poids_total(solut, poids) > capacite:
        return 0
    return calculer_valeur_totale(solut, valeurs)


def generer_population(taille_pop, nbr_objets):
    population = []
    for i in range(taille_pop):
        population.append([random.randint(0, 1) for _ in range(nbr_objets)])
    return population


def selection(population, valeurs, poids, capacite):
    candidats = random.sample(population, 3)
    return max(candidats, key=lambda x: evaluer(x, valeurs, poids, capacite))


def croisement(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]


def mutation(individu, taux_mutation):
    individu = individu[:]
    for i in range(len(individu)):
        if random.random() < taux_mutation:
            individu[i] = 1 - individu[i]
    return individu


def genetic_algorithm(valeurs, capacite, poids, taille_pop, nbr_generations, taux_mutation):
    population = generer_population(taille_pop, len(valeurs))

    meilleur_solut = max(population, key=lambda x: evaluer(x, valeurs, poids, capacite))
    meilleur_valeur = evaluer(meilleur_solut, valeurs, poids, capacite)

    for g in range(nbr_generations):
        population.sort(key=lambda x: evaluer(x, valeurs, poids, capacite), reverse=True)
        nouvelle_population = population[:2]

        while len(nouvelle_population) < taille_pop:
            parent1 = selection(population, valeurs, poids, capacite)
            parent2 = selection(population, valeurs, poids, capacite)
            enfant = croisement(parent1, parent2)
            enfant = mutation(enfant, taux_mutation)
            nouvelle_population.append(enfant)

        population = nouvelle_population

        candidat = max(population, key=lambda x: evaluer(x, valeurs, poids, capacite))
        valeur_candidat = evaluer(candidat, valeurs, poids, capacite)
        if valeur_candidat > meilleur_valeur:
            meilleur_solut = candidat[:]
            meilleur_valeur = valeur_candidat

    return meilleur_solut, meilleur_valeur


valeurs = [14, 9, 20, 6, 11, 16, 8, 13, 5]
poids = [4, 3, 7, 2, 5, 6, 3, 5, 1]
capacite = 18

taille_pop = 50
nbr_generations = 100
taux_mutation = 0.1

random.seed(42)
meilleur_solut, meilleur_valeur = genetic_algorithm(valeurs, capacite, poids,
                                                    taille_pop, nbr_generations, taux_mutation)

print("Meilleure solution trouvée (Algorithme génétique):", meilleur_solut)
print("Valeur maximale:", meilleur_valeur)
print("Poids total:", calculer_poids_total(meilleur_solut, poids))