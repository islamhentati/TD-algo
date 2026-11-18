import random
from collections import deque



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


def generer_voisins(solut, nbr_voisinage):
   
    
    for i in random.sample(range(len(solut)), nbr_voisinage):
        voisin = solut[:]          
        voisin[i] = 1 - voisin[i]  
        v.append(voisin)
    return v


def tabu_search(valeurs, capacite, poids, nbr_iter, taille_tabu, solut_depart, nbr_voisinage, tabu_initial):
    
    meilleur_solut = solution_actuelle[:]
    meilleur_valeur = calculer_valeur_totale(solution_actuelle, valeurs)

    
    tabu_list = deque(maxlen=taille_tabu)
    tabu_list.extend(tabu_initial)

    for i in range(nbr_iter):
      
        v = generer_voisins(solution_actuelle, nbr_voisinage)
       
        v = [voisin for voisin in v if voisin not in tabu_list and calculer_poids_total(voisin, poids) <= capacite]

        if not v:
            break

        solution_actuelle = max(v, key=lambda x: calculer_valeur_totale(x, valeurs))
        valeur_actuelle = calculer_valeur_totale(solution_actuelle, valeurs)

        tabu_list.append(solution_actuelle)

        if valeur_actuelle > meilleur_valeur:
            meilleur_solut = solution_actuelle[:]
            meilleur_valeur = valeur_actuelle

    return meilleur_solut, meilleur_valeur



valeurs = [14, 9, 20, 6, 11, 16, 8, 13, 5]
poids = [4, 3, 7, 2, 5, 6, 3, 5, 1]
capacite = 18  

solut_depart = [1, 0, 0, 1, 0, 0, 1, 0, 0]  
tabu_initial = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 0, 1, 0, 0]]  

nbr_iter = 100     
taille_tabu = 10    
nbr_voisinage = 9    

random.seed(42)
meilleur_solut, meilleur_valeur = tabu_search(valeurs, capacite, poids, nbr_iter, taille_tabu,
                                              solut_depart, nbr_voisinage, tabu_initial)

print("Meilleure solution trouvée (Tabu Search):", meilleur_solut)
print("Valeur maximale:", meilleur_valeur)
print("Poids total:", calculer_poids_total(meilleur_solut, poids))