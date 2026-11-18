import random
from collections import deque


def calculer_cout_total(solut, couts):
    cout = 0
    for i in range(len(solut)):
        for j in range(len(solut[0])):
            cout += solut[i][j] * couts[i][j]
    return cout


def generer_voisins(solut, nbr_voisinage):
    v = []
    while len(v) < nbr_voisinage:
        a, b = random.sample(range(len(solut)), 2)
        j, k = random.sample(range(len(solut[0])), 2)
        if solut[a][j] > 0 and solut[b][k] > 0:
            voisin = [ligne[:] for ligne in solut]
            voisin[a][j] -= 1
            voisin[b][j] += 1
            voisin[b][k] -= 1
            voisin[a][k] += 1
            v.append(voisin)
    return v


def tabu_search(couts, nbr_iter, taille_tabu, solut_depart, nbr_voisinage, tabu_initial):
    solution_actuelle = [ligne[:] for ligne in solut_depart]
    meilleur_solut = [ligne[:] for ligne in solution_actuelle]
    meilleur_cout = calculer_cout_total(solution_actuelle, couts)

    tabu_list = deque(maxlen=taille_tabu)
    tabu_list.extend(tabu_initial)

    for i in range(nbr_iter):
        v = generer_voisins(solution_actuelle, nbr_voisinage)
        v = [voisin for voisin in v if voisin not in tabu_list]

        if not v:
            break

        solution_actuelle = min(v, key=lambda x: calculer_cout_total(x, couts))
        cout_actuel = calculer_cout_total(solution_actuelle, couts)

        tabu_list.append(solution_actuelle)

        if cout_actuel < meilleur_cout:
            meilleur_solut = [ligne[:] for ligne in solution_actuelle]
            meilleur_cout = cout_actuel

    return meilleur_solut, meilleur_cout


couts = [
    [5, 3, 4],
    [6, 7, 2]
]
stocks = [8, 9]
demandes = [4, 5, 8]

solut_depart = [
    [4, 4, 0],
    [0, 1, 8]
]
tabu_initial = [[[4, 4, 0], [0, 1, 8]]]

nbr_iter = 200
taille_tabu = 10
nbr_voisinage = 6

random.seed(42)
meilleur_solut, meilleur_cout = tabu_search(couts, nbr_iter, taille_tabu,
                                            solut_depart, nbr_voisinage, tabu_initial)

print("Meilleure solution trouvée (Tabu Search):", meilleur_solut)
print("Containers envoyes par depot:", [sum(ligne) for ligne in meilleur_solut])
print("Containers recus par magasin:", [sum(meilleur_solut[i][j] for i in range(len(stocks))) for j in range(len(demandes))])
print("Cout total minimal:", meilleur_cout)