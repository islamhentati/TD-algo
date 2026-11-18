import math
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


def generer_voisin(solut):
    voisin = solut[:]
    i = random.randrange(len(voisin))
    voisin[i] = 1 - voisin[i]
    return voisin


def simulated_annealing(valeurs, capacite, poids, solut_depart, temp_initiale, temp_finale, alpha, nbr_iter_palier):
    solution_actuelle = solut_depart[:]
    valeur_actuelle = calculer_valeur_totale(solution_actuelle, valeurs)
    meilleur_solut = solution_actuelle[:]
    meilleur_valeur = valeur_actuelle

    temperature = temp_initiale

    while temperature > temp_finale:
        for i in range(nbr_iter_palier):
            voisin = generer_voisin(solution_actuelle)

            if calculer_poids_total(voisin, poids) > capacite:
                continue

            valeur_voisin = calculer_valeur_totale(voisin, valeurs)
            delta = valeur_voisin - valeur_actuelle

            if delta > 0 or random.random() < math.exp(delta / temperature):
                solution_actuelle = voisin
                valeur_actuelle = valeur_voisin

                if valeur_actuelle > meilleur_valeur:
                    meilleur_solut = solution_actuelle[:]
                    meilleur_valeur = valeur_actuelle

        temperature *= alpha

    return meilleur_solut, meilleur_valeur


valeurs = [14, 9, 20, 6, 11, 16, 8, 13, 5]
poids = [4, 3, 7, 2, 5, 6, 3, 5, 1]
capacite = 18

solut_depart = [1, 0, 0, 1, 0, 0, 1, 0, 0]

temp_initiale = 50
temp_finale = 0.01
alpha = 0.95
nbr_iter_palier = 50

random.seed(42)
meilleur_solut, meilleur_valeur = simulated_annealing(valeurs, capacite, poids, solut_depart,
                                                      temp_initiale, temp_finale, alpha, nbr_iter_palier)

print("Meilleure solution trouvée (Recuit simulé):", meilleur_solut)
print("Valeur maximale:", meilleur_valeur)
print("Poids total:", calculer_poids_total(meilleur_solut, poids))