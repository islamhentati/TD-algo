# TSP : Problème du voyageur de commerce

Un voyageur doit visiter **7 villes** exactement une fois chacune et revenir
à sa ville de départ. Certaines villes ne sont pas reliées par une route
(`INF` dans la matrice). Le but est de trouver le **circuit de distance minimale**.

Le problème est résolu avec trois métaheuristiques, sur la même matrice de distances.

## Données

Matrice symétrique, la ville 1 correspond à l'indice 0. `-` = pas de route.

| | V1 | V2 | V3 | V4 | V5 | V6 | V7 |
|---|---|---|---|---|---|---|---|
| **V1** | 0 | 12 | 10 | - | - | - | 12 |
| **V2** | 12 | 0 | 8 | 12 | - | - | - |
| **V3** | 10 | 8 | 0 | 3 | 9 | - | - |
| **V4** | - | 12 | 3 | 0 | 11 | 7 | - |
| **V5** | - | - | 9 | 11 | 0 | 10 | 6 |
| **V6** | - | - | - | 7 | 10 | 0 | 9 |
| **V7** | 12 | - | - | - | 6 | 9 | 0 |

## Fichiers

| Fichier | Algorithme | Idée principale |
|---|---|---|
| [`genetique.py`](./genetique.py) | Algorithme génétique | Population de circuits, sélection par tournoi, croisement OX, mutation par échange, élitisme |
| [`recuit_simule.py`](./recuit_simule.py) | Recuit simulé | Voisin par échange de deux villes, acceptation d'une moins bonne solution avec la probabilité `exp(-Δ/T)`, refroidissement géométrique |
| [`tabou.py`](./recherche_tabou.py) | Recherche tabou | Meilleur voisin non tabou, liste tabou de taille fixe (`deque`) |

## Exécution

```bash
python genetique.py
python recuit_simule.py
python recherche_tabou.py
```

## Résultats

| Algorithme | Circuit (indices) | Distance |
|---|---|---|
| Génétique | `[1, 0, 6, 4, 5, 3, 2]` | 58 |
| Recuit simulé | `[0, 1, 2, 3, 5, 4, 6]` | 58 |
| Recherche tabou | `[0, 1, 2, 3, 5, 4, 6]` | 58 |

La distance **58** est l'optimum (vérifié par énumération de toutes les permutations).
Les circuits du génétique et des deux autres sont le même cycle, parcouru à partir d'un point de départ différent.

## Paramètres

| Algorithme | Paramètres |
|---|---|
| Génétique | population = 50, générations = 100, taux de mutation = 0.2 |
| Recuit simulé | T initiale = 100, T finale = 0.01, alpha = 0.95, 50 itérations par palier |
| Recherche tabou | 50 itérations, taille de la liste tabou = 10 |