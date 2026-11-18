# Algorithme génétique : grille de jetons

## Description

Ce projet utilise un **algorithme génétique** pour placer **10 jetons** sur une grille de **5 x 5** cases de façon que **chaque ligne et chaque colonne contienne un nombre pair de jetons**.

## Le problème

- Grille de `n x n` cases avec `n = 5`.
- `k = 10` jetons à placer (un jeton par case au maximum).
- Contrainte : le nombre de jetons de chaque ligne et de chaque colonne doit être **pair** (0, 2 ou 4).
- Taille de l'espace de recherche : C(25, 10) = 3 268 760 possibilités.

## Représentation

- Un **individu** (chromosome) est une liste de 25 bits : `1` = jeton, `0` = case vide. La case (ligne, colonne) est à la position `ligne * n + colonne`.
- Tous les individus ont exactement `k` jetons.
- Une **génération** est un ensemble de 70 individus uniques.

## Paramètres

| Paramètre | Valeur |
|---|---|
| `n` | 5 |
| `k` | 10 |
| `nombre_cases` | 25 |
| `nombre_individu` | 70 |
| `max_generation` | 300 |
| `probabilite_croisement` | 0.9 |
| `probabilite_mutation` | 0.3 |

## Fonctions

- `jetons_ligne(individu, i)` / `jetons_colonne(individu, j)` : comptent les jetons d'une ligne / d'une colonne.
- `lignes_colonnes_impaires(individu)` : fitness = nombre de lignes et de colonnes qui contiennent un nombre **impair** de jetons (`0` = solution faisable). On cherche le **minimum**.
- `reparer(individu)` : après un croisement, retire des jetons au hasard (s'il y en a trop) ou en ajoute au hasard (s'il en manque) pour revenir à `k` jetons.
- `creation_individu()` / `createGeneration()` : création de la population initiale (individus uniques).
- `evaluation(generation)` : retourne le meilleur score et la position du meilleur individu.
- `afficheGeneration(generation, nombreGeneration)` : affiche le meilleur individu de la génération.
- `afficheGrille(individu)` : affiche la grille (`X` = jeton, `.` = case vide) avec les jetons par ligne et par colonne.
- `selection(generation)` : choisit les parents.
- `croisement(init, individu1, individu2)` : produit 2 enfants (réparés).
- `mutation(individu)` : déplace un jeton.
- `developpement_generation(parents)` : croisement puis mutation pour former la nouvelle génération.

## Méthodes

Une seule méthode est active pour chaque étape, les autres sont laissées **en commentaire** dans le code.

### Sélection

- **Roulette** (utilisée) : probabilité proportionnelle à `1 / (score + 1)` (plus petit score = plus de chance d'être choisi).
- Tournoi : on tire 3 individus et on garde celui qui a le plus petit score.
- Rang : probabilité proportionnelle au rang (du pire au meilleur).
- Élitiste : seule la moitié la meilleure peut devenir parent.

### Croisement

- **1 point** (utilisé) : début du parent 1 + fin du parent 2 (et inversement).
- 2 points : le morceau entre 2 points est échangé.
- Uniforme : un masque 0/1 choisit le parent qui donne chaque case.

### Mutation

Un jeton est déplacé : une case avec jeton devient vide et une case vide reçoit le jeton (le nombre de jetons reste `k`), avec une probabilité de 0.3.

## Fonctionnement

1. Création de la génération initiale.
2. Sélection des parents (roulette).
3. Croisement (avec réparation) puis mutation pour créer la nouvelle génération.
4. Élitisme : le meilleur individu trouvé depuis le début est remis dans la génération.
5. Arrêt quand une solution faisable est trouvée (score = 0) ou quand `max_generation` est dépassé.

## Exécution

```bash
python genetique.py
```

## Exemple de résultat

```
taille de l'espace de recherche : C(25, 10 ) = 3268760
le meilleur score est : 0
nombre de generations : 0
X . . . X   jetons: 2
X X . . .   jetons: 2
. X . . X   jetons: 2
. . X . X   jetons: 2
. . X . X   jetons: 2
2 2 2 0 4   <- jetons par colonne
solution faisable : chaque ligne et chaque colonne a un nombre pair de jetons
```

Le résultat varie d'une exécution à l'autre (nombre de générations, grille trouvée).