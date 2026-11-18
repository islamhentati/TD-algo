import math
import random


def calculer_cout_total(solut, couts):
    cout = 0
    for i in range(len(solut)):
        for j in range(len(solut[0])):
            cout += solut[i][j] * couts[i][j]
    return cout


def generer_voisin(solut):
    while True:
        a, b = random.sample(range(len(solut)), 2)
        j, k = random.sample(range(len(solut[0])), 2)
        if solut[a][j] > 0 and solut[b][k] > 0:
            voisin = [ligne[:] for ligne in solut]
            voisin[a][j] -= 1
            voisin[b][j] += 1
            voisin[b][k] -= 1
            voisin[a][k] += 1
            return voisin


def recuit_simule(couts, solut_depart, temp_initiale, temp_finale, alpha, nbr_iter_palier):
    solution_actuelle = [ligne[:] for ligne in solut_depart]
    cout_actuel = calculer_cout_total(solution_actuelle, couts)
    meilleur_solut = [ligne[:] for ligne in solution_actuelle]
    meilleur_cout = cout_actuel

    temperature = temp_initiale

    while temperature > temp_finale:
        for i in range(nbr_iter_palier):
            voisin = generer_voisin(solution_actuelle)
            cout_voisin = calculer_cout_total(voisin, couts)
            delta = cout_voisin - cout_actuel

            if delta < 0 or random.random() < math.exp(-delta / temperature):
                solution_actuelle = voisin
                cout_actuel = cout_voisin

                if cout_actuel < meilleur_cout:
                    meilleur_solut = [ligne[:] for ligne in solution_actuelle]
                    meilleur_cout = cout_actuel

        temperature *= alpha

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

temp_initiale = 20
temp_finale = 0.01
alpha = 0.95
nbr_iter_palier = 50

random.seed(42)
meilleur_solut, meilleur_cout = recuit_simule(couts, solut_depart, temp_initiale,
                                                    temp_finale, alpha, nbr_iter_palier)

print("Meilleure solution trouvée (Recuit simulé):", meilleur_solut)
print("Containers envoyes par depot:", [sum(ligne) for ligne in meilleur_solut])
print("Containers recus par magasin:", [sum(meilleur_solut[i][j] for i in range(len(stocks))) for j in range(len(demandes))])
print("Cout total minimal:", meilleur_cout)