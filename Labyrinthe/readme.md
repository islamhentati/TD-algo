# Algorithme génétique : sortie d'un labyrinthe

## Description

Ce projet utilise un **algorithme génétique** pour trouver le chemin d'un robot entre l'**entrée** (case (1,1)) et la **sortie** (case (10,10)) d'un labyrinthe de 10 x 10 cases.

## Le labyrinthe

`1` = mur (case tramée), `0` = case libre (case blanche).

```
0 0 0 1 0 0 0 0 0 0
1 1 0 1 0 1 1 1 1 0
0 0 0 0 0 0 0 0 1 0
0 1 1 1 1 1 1 0 1 0
0 0 0 0 0 0 1 0 0 0
1 1 1 1 1 0 1 1 1 0
0 0 0 0 0 0 0 0 1 0
0 1 1 1 1 1 1 0 1 0
0 0 0 0 0 0 1 0 0 0
1 1 1 1 1 0 0 0 1 0
```

## Représentation

- Un **individu** (chromosome) est une liste de 40 déplacements : `0` = haut, `1` = bas, `2` = gauche, `3` = droite.
- Une **génération** est un ensemble de 70 individus uniques.
- Le robot s'arrête s'il se cogne contre un mur (ou le bord), s'il revient sur une case déjà visitée, ou s'il atteint la sortie.

## Paramètres

| Paramètre | Valeur |
|---|---|
| `nombre_deplacements` | 40 |
| `nombre_individu` | 70 |
| `max_generation` | 300 |
| `probabilite_croisement` | 0.9 |
| `probabilite_mutation` | 0.3 |

## Fonctions

- `parcours(individu)` : fait marcher le robot et retourne le chemin parcouru.
- `calculer_distances()` : parcours en largeur à partir de la sortie, donne pour chaque case libre le nombre de déplacements restants (la distance de Manhattan piégerait le robot dans les impasses).
- `distance_sortie(individu)` : fitness = distance restante entre la dernière case atteinte et la sortie (`0` = sortie atteinte). On cherche le **minimum**.
- `creation_individu()` / `createGeneration()` : création de la population initiale (individus uniques).
- `evaluation(generation)` : retourne le meilleur score et la position du meilleur individu.
- `afficheGeneration(generation, nombreGeneration)` : affiche le meilleur individu de la génération.
- `selection(generation)` : choisit les parents.
- `croisement(init, individu1, individu2)` : produit 2 enfants.
- `mutation(individu)` : change un déplacement au hasard.
- `developpement_generation(parents)` : croisement puis mutation pour former la nouvelle génération.

## Méthodes

Une seule méthode est active pour chaque étape, les autres sont laissées **en commentaire** dans le code.

### Sélection

- **Roulette** (utilisée) : probabilité proportionnelle à `1 / (distance + 1)` (plus petite distance = plus de chance d'être choisi).
- Tournoi : on tire 3 individus et on garde celui qui a la plus petite distance.
- Rang : probabilité proportionnelle au rang (du pire au meilleur).
- Élitiste : seule la moitié la meilleure peut devenir parent.

### Croisement

- **1 point** (utilisé) : début du parent 1 + fin du parent 2 (et inversement).
- 2 points : le morceau entre 2 points est échangé.
- Uniforme : un masque 0/1 choisit le parent qui donne chaque déplacement.

### Mutation

Un déplacement choisi au hasard est remplacé par un autre, avec une probabilité de 0.3.

## Fonctionnement

1. Création de la génération initiale.
2. Sélection des parents (roulette).
3. Croisement puis mutation pour créer la nouvelle génération.
4. Élitisme : le meilleur individu trouvé depuis le début est remis dans la génération.
5. Arrêt quand la sortie est atteinte (distance = 0) ou quand `max_generation` est dépassé.

## Exécution

```bash
python genetique.py
```

## Exemple de résultat

```
le meilleur score est : 0
le chemin (ligne, colonne) est : [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (4, 8), (5, 8), (5, 9), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10)]
la sortie est atteinte en 18 deplacements
```

Le résultat varie d'une exécution à l'autre (nombre de générations, chemin trouvé).