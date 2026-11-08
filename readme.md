# Cédule de maintenance par algorithme génétique

Programme Python qui planifie la maintenance de centrales électriques à l'aide d'un algorithme génétique. L'objectif est de trouver une cédule qui **maximise la plus petite réserve de puissance** pendant l'année.

Le projet est basé sur l'exemple « cédule de maintenance » . Il utilise la **sélection par loterie** (roulette) et propose trois types de mutation, dont la **mutation par inversion**.

---


## 1. Contenu du projet

| Fichier | Description |
|---|---|
| `cedule.py` | Code complet de l'algorithme génétique |
| `README.md` |  document |

## 2.exécution


Le script effectue dans l'ordre :

1. **Vérification de l'exemple du cours** : le chromosome `0110 0011 0001 1000 0100 0010 1000` doit donner des réserves de 20, 25, 35 et 30 MW, donc une performance de 20 MW.
2. **Comparaison des trois mutations** : chacune est exécutée 20 fois, et le programme affiche la moyenne et le meilleur résultat.
3. **Affichage détaillé de la meilleure cédule** trouvée avec la sélection par loterie et la mutation par inversion.

## 3. Description du problème

On doit planifier la maintenance de 7 centrales électriques. Chaque centrale doit être arrêtée pendant un certain nombre d'intervalles pour sa maintenance préventive.

| Unité | Capacité (MW) | Intervalles de maintenance requis |
|---|---|---|
| 1 | 20 | 2 |
| 2 | 15 | 2 |
| 3 | 35 | 1 |
| 4 | 40 | 1 |
| 5 | 15 | 1 |
| 6 | 15 | 1 |
| 7 | 10 | 1 |

- **Capacité totale** : 150 MW.
- **Découpage de l'année** : 4 intervalles, avec une demande en puissance de **80, 90, 65 et 70 MW** respectivement.

**Contraintes**

- La maintenance d'une unité commence au début d'un intervalle et se termine à la fin d'un intervalle.
- Une unité qui a besoin de 2 intervalles les utilise de façon consécutive.
- La réserve de puissance pendant un intervalle doit être plus grande que la demande, c'est-à-dire que la réserve calculée ne doit pas être négative.

**Calcul de la réserve** pour un intervalle :

```
Réserve = Capacité totale − Puissance perdue (unités en maintenance) − Demande
```

## 4. Modélisation

### 4.1 Encodage

Chaque unité est représentée par un **gène de 4 bits**, un bit par intervalle :

- `1` : l'unité est en maintenance pendant cet intervalle ;
- `0` : l'unité n'est pas en maintenance.

Exemple : pour l'unité 1, le gène `1100` signifie maintenance pendant les intervalles 1 et 2.

```
 bit :   1   1   0   0
         |   |   |   |
 intervalle 1 | intervalle 3
            intervalle 2   intervalle 4
```

Un **chromosome** est la suite des 7 gènes, soit 28 bits. Dans le code, c'est une liste plate de 28 entiers (0 ou 1).

### 4.2 Gènes valides

Seuls les gènes qui respectent la durée de maintenance et la contrainte de continuité sont permis :

| Unité | Gènes valides |
|---|---|
| 1 | `1100`, `0110`, `0011` |
| 2 | `1100`, `0110`, `0011` |
| 3 à 7 | `1000`, `0100`, `0010`, `0001` |

### 4.3 Exemple de chromosome

```
 Unité 1   Unité 2   Unité 3   Unité 4   Unité 5   Unité 6   Unité 7
  0110      0011      0001      1000      0100      0010      1000
```

### 4.4 Création de la population initiale

Pour chaque individu et chaque unité, un gène valide est tiré au hasard. Tous les individus de départ respectent donc les contraintes de durée et de continuité.

## 5. Fonction objective

Pour un chromosome donné, on calcule la puissance en maintenance de chaque intervalle, puis la réserve.

**Exemple avec le chromosome du cours** `0110 0011 0001 1000 0100 0010 1000` :

| Intervalle | Unités en maintenance | Puissance perdue | Calcul | Réserve |
|---|---|---|---|---|
| 1 | 4 et 7 | 40 + 10 = 50 MW | 150 − 50 − 80 | **20 MW** |
| 2 | 1 et 5 | 20 + 15 = 35 MW | 150 − 35 − 90 | **25 MW** |
| 3 | 1, 2 et 6 | 20 + 15 + 15 = 50 MW | 150 − 50 − 65 | **35 MW** |
| 4 | 2 et 3 | 15 + 35 = 50 MW | 150 − 50 − 70 | **30 MW** |

La **performance** (fitness) du chromosome est la **plus petite réserve** : ici **20 MW**.

Si une réserve est négative, la performance vaut **0**. Cela pénalise les cédules qui ne couvrent pas la demande.

## 6. Sélection par loterie

La sélection par loterie (roulette wheel) donne à chaque individu une part de la roue proportionnelle à sa performance.

**Exemple** avec 4 individus :

| Individu | Performance | Part de la roue |
|---|---|---|
| A | 20 | 40 % |
| B | 25 | 50 % |
| C | 5 | 10 % |
| D | 0 | 0 % |

**Fonctionnement dans le code** (`selection_loterie`) :

1. On calcule la somme des performances de la population.
2. On tire un nombre au hasard entre 0 et cette somme (la « bille » de la roulette).
3. On parcourt la population en cumulant les performances, et on retient le premier individu dont le cumul atteint ce nombre.
4. On répète pour obtenir un second parent.

**Cas particulier** : si tous les individus ont une performance de 0, la somme est nulle et la roue n'a plus de sens. Le programme tire alors les parents de façon uniforme.

Les meilleurs individus ont donc plus de chances d'être choisis, mais les moins bons gardent une chance, ce qui préserve la diversité de la population.

## 7. Croisement

Le croisement est à **un point**, et il ne peut se faire qu'**entre deux blocs de 4 bits**. Couper à l'intérieur d'un gène produirait des maintenances illogiques ou fausses (par exemple `1010`).

Il est appliqué avec la probabilité `p_croisement`. Sinon, les enfants sont des copies des parents.

**Exemple** (point de croisement après le 4e gène) :

```
Parent 1 :  0110 0011 0001 1000 | 0100 0010 1000
Parent 2 :  1100 0110 0100 0001 | 0010 1000 0100
                                ^ point de croisement

Rejeton 1 : 0110 0011 0001 1000 | 0010 1000 0100
Rejeton 2 : 1100 0110 0100 0001 | 0100 0010 1000
```

Chaque rejeton garde le début d'un parent et reçoit la fin de l'autre. Comme chaque gène reste à sa place (le gène numéro *k* correspond toujours à l'unité *k*), les rejetons restent valides.

## 8. Mutations

La mutation est appliquée **gène par gène** avec la probabilité `p_mutation`. Trois types sont disponibles, et on choisit avec le paramètre `type_mutation`.

### 8.1 Mutation par inversion (`"inversion"`)

On inverse l'**ordre des bits** d'un gène.

| Avant | Après |
|---|---|
| `1100` | `0011` |
| `0011` | `1100` |
| `1000` | `0001` |
| `0001` | `1000` |
| `0100` | `0010` |
| `0010` | `0100` |
| `0110` | `0110` (inchangé, car symétrique) |

L'avantage est que **le gène obtenu est toujours valide** : l'inverse d'un gène permis est lui aussi permis. La mutation décale la maintenance vers l'autre extrémité de l'année sans jamais casser les contraintes.

### 8.2 Mutation par remplacement (`"remplacement"`)

C'est la mutation de l'exemple du cours. Le gène est remplacé par **un autre gène valide** de la même unité, choisi au hasard.

```
0110 0011 0001 1000 0100 0010 1000
          ^^^^
          0001 est remplacé par 0100
0110 0011 0100 1000 0100 0010 1000
```

### 8.3 Mutation par échange (`"echange"`)

On échange les gènes de **deux unités qui ont les mêmes options** (les unités 1 et 2 entre elles, ou deux unités parmi les unités 3 à 7). Les puissances des unités étant différentes, cet échange modifie bien la cédule tout en gardant des gènes valides.

## 9. Déroulement de l'algorithme

```
1. Créer une population initiale de chromosomes valides
2. Pour chaque génération :
     a. Évaluer la performance de chaque individu
     b. Mémoriser le meilleur individu rencontré
     c. Construire la nouvelle population :
          - (élitisme) y placer d'abord une copie du meilleur individu
          - tant qu'elle n'est pas pleine :
              * choisir 2 parents par loterie
              * les croiser (probabilité p_croisement)
              * muter les deux rejetons (probabilité p_mutation par gène)
              * ajouter les rejetons à la nouvelle population
     d. Remplacer l'ancienne population par la nouvelle
3. Retourner le meilleur individu trouvé
```

L'**élitisme** garantit que la meilleure solution trouvée n'est jamais perdue d'une génération à l'autre.

## 10. Structure du code

| Fonction | Rôle |
|---|---|
| `creer_chromosome()` | Crée un chromosome aléatoire valide |
| `gene(chromo, i)` | Retourne le gène (bloc de 4 bits) de l'unité `i` |
| `set_gene(chromo, i, bits)` | Remplace le gène de l'unité `i` |
| `afficher(chromo)` | Affiche le chromosome en blocs de 4 bits |
| `reserves(chromo)` | Calcule la réserve de chaque intervalle |
| `fitness(chromo)` | Retourne la plus petite réserve (0 si négative) |
| `selection_loterie(population, fits)` | Sélection par loterie de deux parents |
| `croisement(p1, p2, p_croisement)` | Croisement à un point aux frontières de blocs |
| `mutation_inversion(chromo, p)` | Mutation par inversion des bits d'un gène |
| `mutation_remplacement(chromo, p)` | Remplacement par un autre gène valide |
| `mutation_echange(chromo, p)` | Échange de gènes entre unités équivalentes |
| `algorithme_genetique(...)` | Boucle principale de l'algorithme |
| `rapport(chromo)` | Affiche le détail d'une cédule |

Les données du problème sont en haut du fichier (`CAPACITES`, `NB_INTERVALLES_MAINT`, `DEMANDE`). On peut les modifier pour résoudre une autre instance. Le dictionnaire `MUTATIONS` relie le nom de chaque mutation à sa fonction.

## 11. Paramètres

| Paramètre | Valeur par défaut | Rôle |
|---|---|---|
| `taille_pop` | 45 | Taille de la population. Règle générale du cours : environ 6 à 7 fois le nombre de variables (ici 7 unités) |
| `n_generations` | 100 | Nombre de générations |
| `p_croisement` | 0.8 | Probabilité de croiser un couple de parents |
| `p_mutation` | 0.1 | Probabilité de mutation de chaque gène |
| `type_mutation` | `"inversion"` | `"inversion"`, `"remplacement"` ou `"echange"` |
| `elitisme` | `True` | Conserve le meilleur individu à chaque génération |
| `graine` | `None` | Graine du générateur aléatoire, pour reproduire un résultat |

Comme le recommande le cours, il ne faut pas se limiter à une seule valeur pour les probabilités de croisement et de mutation : on commence avec une valeur standard, puis on en essaie d'autres.

## 12. Utilisation dans votre propre code

```python
from cedule_maintenance_ga import algorithme_genetique, rapport, fitness

meilleur, hist_best, hist_moy = algorithme_genetique(
    taille_pop=45,
    n_generations=100,
    p_croisement=0.8,
    p_mutation=0.1,
    type_mutation="inversion",
    elitisme=True,
    graine=42,
)

rapport(meilleur)
print("Performance :", fitness(meilleur), "MW")
```

La fonction retourne trois valeurs :

- le meilleur chromosome trouvé ;
- la liste de la meilleure performance de chaque génération ;
- la liste de la performance moyenne de chaque génération.

## 13. Résultats

### Exemple d'affichage

```
=== Exemple du cours ===
Chromosome : 0110 0011 0001 1000 0100 0010 1000
  Intervalle 1 : unités en maintenance [4, 7] | réserve = 20 MW
  Intervalle 2 : unités en maintenance [1, 5] | réserve = 25 MW
  Intervalle 3 : unités en maintenance [1, 2, 6] | réserve = 35 MW
  Intervalle 4 : unités en maintenance [2, 3] | réserve = 30 MW
  Performance (plus petite réserve) = 20 MW

=== Comparaison des mutations (20 exécutions chacune) ===
inversion    : moyenne = 25.00 MW | meilleur = 25 MW
remplacement : moyenne = 24.75 MW | meilleur = 25 MW
echange      : moyenne = 25.00 MW | meilleur = 25 MW

=== Meilleure cédule (sélection loterie + mutation inversion) ===
Chromosome : 1100 0110 0010 0001 0001 1000 0010
  Intervalle 1 : unités en maintenance [1, 6] | réserve = 35 MW
  Intervalle 2 : unités en maintenance [1, 2] | réserve = 25 MW
  Intervalle 3 : unités en maintenance [2, 3, 7] | réserve = 25 MW
  Intervalle 4 : unités en maintenance [4, 5] | réserve = 25 MW
  Performance (plus petite réserve) = 25 MW
```

### 25 MW est l'optimum

Le calcul suivant montre qu'on ne peut pas faire mieux que 25 MW :

- Puissance totale en maintenance : 20×2 + 15×2 + 35 + 40 + 15 + 15 + 10 = **185 MW**
- Puissance disponible sur les 4 intervalles : 4 × 150 − 185 = **415 MW**
- Demande totale : 80 + 90 + 65 + 70 = **305 MW**
- Réserve totale : 415 − 305 = **110 MW**

La plus petite réserve ne peut pas dépasser 110 / 4 = 27,5 MW. Toutes les capacités étant des multiples de 5, la meilleure valeur possible est **25 MW**, et l'algorithme l'atteint.

### Comparaison des mutations

Sur ce petit problème, les trois mutations atteignent l'optimum. L'inversion et l'échange le trouvent à chaque exécution. Le remplacement est à 24,75 de moyenne, donc une exécution sur 20 s'est arrêtée à 20 MW. L'écart est trop faible pour conclure qu'un type de mutation est meilleur. Pour mieux les départager, on peut réduire `n_generations` ou `taille_pop`, ou baisser `p_mutation`.

