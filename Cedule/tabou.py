import random
from collections import deque


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


def generer_voisins(solut, choix, nbr_voisinage):
    v = []
    for i in random.sample(range(len(solut)), nbr_voisinage):
        voisin = solut[:]
        autres = [g for g in choix[i] if g != solut[i]]
        voisin[i] = random.choice(autres)
        v.append(voisin)
    return v


def tabu_search(capacites, demandes, choix, nbr_iter, taille_tabu, solut_depart, nbr_voisinage, tabu_initial):
    solution_actuelle = solut_depart[:]
    meilleur_solut = solution_actuelle[:]
    meilleur_perf = calculer_performance(solution_actuelle, capacites, demandes)

    tabu_list = deque(maxlen=taille_tabu)
    tabu_list.extend(tabu_initial)

    for i in range(nbr_iter):
        v = generer_voisins(solution_actuelle, choix, nbr_voisinage)
        v = [voisin for voisin in v if voisin not in tabu_list and min(calculer_reserves(voisin, capacites, demandes)) >= 0]

        if not v:
            break

        solution_actuelle = max(v, key=lambda x: calculer_performance(x, capacites, demandes))
        perf_actuelle = calculer_performance(solution_actuelle, capacites, demandes)

        tabu_list.append(solution_actuelle)

        if perf_actuelle > meilleur_perf:
            meilleur_solut = solution_actuelle[:]
            meilleur_perf = perf_actuelle

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
tabu_initial = [["0110", "0011", "0001", "1000", "0100", "0010", "1000"]]

nbr_iter = 200
taille_tabu = 10
nbr_voisinage = 7

random.seed(42)
meilleur_solut, meilleur_perf = tabu_search(capacites, demandes, choix, nbr_iter, taille_tabu,
                                            solut_depart, nbr_voisinage, tabu_initial)

print("Meilleure solution trouvée (Tabu Search):", meilleur_solut)
print("Reserves par intervalle:", calculer_reserves(meilleur_solut, capacites, demandes))
print("Performance (plus petite reserve):", meilleur_perf)