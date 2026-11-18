# Cédule de maintenance

On doit planifier la maintenance de **7 centrales électriques** sur une année
séparée en **4 intervalles**. Chaque centrale doit être en maintenance pendant un
certain nombre d'intervalles consécutifs. Pendant la maintenance, sa puissance
est perdue. Le but est de **maximiser la réserve de puissance** de l'année.

```
Réserve (intervalle) = Capacité totale - Puissance en maintenance - Demande
```

La demande doit toujours être couverte : une réserve négative rend la cédule invalide.

## Données

| Unité | Capacité (MW) | Intervalles de maintenance requis |
|---|---|---|
| 1 | 30 | 2 |
| 2 | 20 | 2 |
| 3 | 25 | 1 |
| 4 | 40 | 1 |
| 5 | 15 | 1 |
| 6 | 10 | 1 |
| 7 | 20 | 1 |

Capacité totale : **160 MW**.

| Intervalle | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **Demande (MW)** | 85 | 90 | 70 | 75 |

## Encodage

Une solution est une liste de 7 gènes de 4 bits, un par unité. Le bit `1` veut dire
« en maintenance pendant cet intervalle ». Les gènes possibles sont :

| Unité | Maintenance possible |
|---|---|
| 1 et 2 | `1100`, `0110`, `0011` |
| 3 à 7 | `1000`, `0100`, `0010`, `0001` |

Exemple : `["0110", "0011", "0001", "1000", "0100", "0010", "1000"]`
donne les réserves `[15, 25, 30, 40]`.

## Fonction objectif

La **performance** d'une solution est la **plus petite réserve** parmi les 4 intervalles
(0 si une réserve est négative). On cherche à la maximiser.
L'exemple ci-dessus a donc une performance de 15.

## Fichiers

| Fichier | Algorithme | Idée principale |
|---|---|---|
| [`genetique.py`](./genetique.py) | Algorithme génétique | **Sélection par roulette** (probabilité proportionnelle à la performance), croisement à un point sur les blocs de 4 bits, mutation d'un gène vers un autre gène permis, la meilleure cédule est gardée à chaque génération |
| [`recuit_simule.py`](./recuit_simule.py) | Recuit simulé | Voisin = une unité change de période de maintenance, acceptation d'une moins bonne solution avec la probabilité `exp(Δ/T)`, refroidissement géométrique |
| [`recherche_tabou.py`](./recherche_tabou.py) | Recherche tabou | Voisins = une unité change de période, voisins tabous ou invalides éliminés, meilleur voisin choisi, liste tabou de taille fixe (`deque`) |

## Exécution

```bash
python genetique.py
python recuit_simule.py
python tabou.py
```

## Résultats

| Algorithme | Solution | Réserves | Performance |
|---|---|---|---|
| Génétique | `['0011', '0110', '0001', '1000', '0010', '1000', '0100']` | [25, 30, 25, 30] | 25 |
| Recuit simulé | `['0011', '0011', '1000', '0100', '0010', '0001', '1000']` | [30, 30, 25, 25] | 25 |
| Recherche tabou | `['0011', '0011', '0100', '1000', '0010', '0001', '0100']` | [35, 25, 25, 25] | 25 |

La performance **25** est l'optimum (vérifié par énumération des 9216 cédules possibles,
dont 3383 sont valides). 14 cédules différentes atteignent cette valeur, c'est pourquoi
les trois solutions ne sont pas identiques.

## Paramètres

| Algorithme | Paramètres |
|---|---|
| Génétique | population = 100, générations = 100, taux de mutation = 0.3, point de croisement tiré au hasard à chaque génération |
| Recuit simulé | T initiale = 20, T finale = 0.01, alpha = 0.95, 50 voisins par palier |
| Recherche tabou | 200 itérations, liste tabou = 10, 7 voisins par itération |

Le recuit simulé et la recherche tabou partent de la cédule de l'exemple (performance 15).
Le génétique part d'une population aléatoire.
`random.seed(42)` fixe le hasard pour que les résultats soient reproductibles.