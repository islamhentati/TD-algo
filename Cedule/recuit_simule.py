import math
import random


def calculer_reserves(solut, capacites, demandes):
    capacite_totale = sum(capacites)
    reserves = []
    for t in range(len(demandes)):
        perdue = 0
        for u in range(len(solut)):
            if solut[u][t] == "1":
                perdue += capacites[u]
        reserves.append(capacite_totale - perdue - demandes[t])
    return reserves


def calculer_performance(solut, capacites, demandes):
    p = min(calculer_reserves(solut, capacites, demandes))
    if p < 0:
        return 0
    return p


def generer_voisin(solut, choix):
    voisin = solut[:]
    i = random.randrange(len(voisin))
    autres = [g for g in choix[i] if g != solut[i]]
    voisin[i] = random.choice(autres)
    return voisin


def recuit_simule(capacites, demandes, choix, solut_depart, temp_initiale, temp_finale, alpha, nbr_iter_palier):
    solution_actuelle = solut_depart[:]
    perf_actuelle = calculer_performance(solution_actuelle, capacites, demandes)
    meilleur_solut = solution_actuelle[:]
    meilleur_perf = perf_actuelle

    temperature = temp_initiale

    while temperature > temp_finale:
        for i in range(nbr_iter_palier):
            voisin = generer_voisin(solution_actuelle, choix)

            if min(calculer_reserves(voisin, capacites, demandes)) < 0:
                continue

            perf_voisin = calculer_performance(voisin, capacites, demandes)
            delta = perf_voisin - perf_actuelle

            if delta > 0 or random.random() < math.exp(delta / temperature):
                solution_actuelle = voisin
                perf_actuelle = perf_voisin

                if perf_actuelle > meilleur_perf:
                    meilleur_solut = solution_actuelle[:]
                    meilleur_perf = perf_actuelle

        temperature *= alpha

    return meilleur_solut, meilleur_perf


capacites = [30, 20, 25, 40, 15, 10, 20]
demandes = [85, 90, 70, 75]

choix = [
    ["1100", "0110", "0011"],
    ["1100", "0110", "0011"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"]
]

solut_depart = ["0110", "0011", "0001", "1000", "0100", "0010", "1000"]

temp_initiale = 20
temp_finale = 0.01
alpha = 0.95
nbr_iter_palier = 50

random.seed(42)
meilleur_solut, meilleur_perf = recuit_simule(capacites, demandes, choix, solut_depart,
                                                    temp_initiale, temp_finale, alpha, nbr_iter_palier)

print("Meilleure solution trouvée (Recuit simulé):", meilleur_solut)
print("Reserves par intervalle:", calculer_reserves(meilleur_solut, capacites, demandes))
print("Performance (plus petite reserve):", meilleur_perf)