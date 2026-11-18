# Dépôts et magasins (problème de transport)

Une entreprise dispose de **2 dépôts** contenant chacun un certain nombre de containers.
**3 magasins** commandent des containers. On connaît le coût de transport d'un container
de chaque dépôt vers chaque magasin. Le but est de trouver l'organisation des livraisons
qui **minimise le coût total de transport**.

## Données

| | M1 | M2 | M3 | Stock du dépôt |
|---|---|---|---|---|
| **D1** | 5 | 3 | 4 | 8 |
| **D2** | 6 | 7 | 2 | 9 |
| **Demande** | 4 | 5 | 8 | |

Les coûts sont par container. Le stock total (17) est égal à la demande totale (17).

## Modèle

Soit `x[i][j]` le nombre de containers envoyés du dépôt `Di` vers le magasin `Mj`.

```
Minimiser   somme(coût[i][j] * x[i][j])
Sous les contraintes :
    somme sur j de x[i][j]  <=  stock du dépôt i      (on ne dépasse pas le stock)
    somme sur i de x[i][j]  =   demande du magasin j  (chaque demande est satisfaite)
    x[i][j] entier, >= 0
```

## Représentation

Une solution est une matrice 2 x 3 (une ligne par dépôt, une colonne par magasin), par exemple
`[[3, 5, 0], [1, 0, 8]]` : D1 envoie 3 containers à M1 et 5 à M2, D2 envoie 1 à M1 et 8 à M3.

Pour garder les solutions valides, le voisin d'une solution est obtenu par un **échange** :
un container de `Mj` change de dépôt, et un container de `Mk` fait le chemin inverse.
Les demandes des magasins et les quantités sorties de chaque dépôt ne changent donc pas.

## Fichiers

| Fichier | Algorithme | Idée principale |
|---|---|---|
| [`genetique.py`](./genetique.py) | Algorithme génétique | **Sélection par roulette** (fitness = coût maximal possible - coût de la solution, 0 si le stock est dépassé), croisement par colonnes (magasins), mutation par échange, la meilleure solution est gardée à chaque génération |
| [`recuit_simule.py`](./recuit_simule.py) | Recuit simulé | Voisin par échange, acceptation d'une solution plus chère avec la probabilité `exp(-Δ/T)`, refroidissement géométrique |
| [`recherche_tabou.py`](./recherche_tabou.py) | Recherche tabou | Voisins par échange, voisins tabous éliminés, meilleur voisin choisi (même s'il est moins bon), liste tabou de taille fixe (`deque`) |

## Exécution

```bash
python genetique.py
python recuit_simule.py
python tabou.py
```

## Résultats

| Algorithme | Solution | Coût total |
|---|---|---|
| Génétique | `[[3, 5, 0], [1, 0, 8]]` | 52 |
| Recuit simulé | `[[3, 5, 0], [1, 0, 8]]` | 52 |
| Recherche tabou | `[[3, 5, 0], [1, 0, 8]]` | 52 |

Le coût **52** est l'optimum (vérifié par énumération des 29 solutions valides) :

```
D1 -> M1 : 3 containers   (3 x 5  = 15)
D1 -> M2 : 5 containers   (5 x 3  = 15)
D2 -> M1 : 1 container    (1 x 6  =  6)
D2 -> M3 : 8 containers   (8 x 2  = 16)
                    Total = 52
```

Le dépôt D1 ne peut pas fournir seul M1 et M2 (4 + 5 = 9 containers pour un stock de 8) :
un container de M1 vient donc de D2, car c'est celui qui coûte le moins cher à déplacer (6 - 5 = 1).

## Paramètres

| Algorithme | Paramètres |
|---|---|
| Génétique | population = 50, générations = 100, taux de croisement = 0.8, taux de mutation = 0.3 |
| Recuit simulé | T initiale = 20, T finale = 0.01, alpha = 0.95, 50 voisins par palier |
| Recherche tabou | 200 itérations, liste tabou = 10, 6 voisins par itération |

Le recuit simulé et la recherche tabou partent de la solution `[[4, 4, 0], [0, 1, 8]]` (coût 55).
Le génétique part d'une population aléatoire.
`random.seed(42)` fixe le hasard pour que les résultats soient reproductibles.