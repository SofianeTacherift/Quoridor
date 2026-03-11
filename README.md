# Quoridor — Projet de Graphes (BUT Informatique S2)

## Présentation

Implémentation du jeu de plateau **Quoridor** en Python, avec un bot adversaire basé sur l'algorithme de Dijkstra. Ce projet utilise les graphes comme structure centrale pour modéliser la grille de jeu, gérer les déplacements et alimenter l'intelligence artificielle.

---

## Utilisation des graphes

C'est le cœur du projet. Tout repose sur un graphe NetworkX qui modélise la grille.

### Modélisation de la grille comme graphe

La grille 9×9 est représentée par un graphe non orienté où :

- Chaque **case** `(i, j)` est un **nœud**
- Chaque **connexion entre cases adjacentes** est une **arête**

```python
def initGraphe(self):
    g = Graph()
    for i in range(9):
        for j in range(9):
            g.add_node((i, j))
            if i > 0:
                g.add_edge((i, j), (i-1, j))  # connexion verticale
            if j > 0:
                g.add_edge((i, j), (i, j-1))  # connexion horizontale
    self.graphe = g
```

Ce choix de modélisation permet de traiter naturellement les déplacements et les barrières comme des opérations sur le graphe.

---
# touches
Z déplacement devant <br>
Q déplacement à gauche <br>
D déplacement à droite <br>
S déplacement en bas <br>
E mode barrière <br>
A placer barrière <br>

### Les barrières = suppression d'arêtes

Poser une barrière revient à **supprimer des arêtes** du graphe. C'est l'opération graphe la plus centrale du projet.

- Barrière **horizontale** → supprime les arêtes Nord-Sud entre deux paires de cases
- Barrière **verticale** → supprime les arêtes Est-Ouest entre deux paires de cases

```python
def casserArretes(self, n1, n2):
    if not self.graphe.has_edge(n1, n2):
        return False
    self.graphe.remove_edge(n1, n2)
    return True
```

Retirer une barrière = **restaurer les arêtes** avec `add_edge`.

Une attention particulière est portée à la **cohérence du graphe** : si une seule des deux arêtes d'une barrière peut être cassée, les deux sont restaurées pour éviter un état incohérent.

---

### Vérification de chemin = connexité du graphe

Avant de valider une barrière, on vérifie que **les deux joueurs ont encore un chemin possible** vers leur ligne d'arrivée. C'est une vérification de **connexité partielle** du graphe :

```python
def cheminPossibleJoueur(self, joueur):
    i = 8 if joueur == self.j1 else 0
    for j in range(9):
        if self.dijkstra((joueur.caseY, joueur.caseX), (i, j)) != -1:
            return True
    return False
```

Si la barrière isole un joueur, elle est **annulée** et les arêtes sont restaurées. Cette règle est directement celle du Quoridor réel.

---

### Déplacements validés par le graphe

Les déplacements des joueurs ne sont pas simplement des vérifications de coordonnées — ils interrogent directement **l'existence d'une arête** dans le graphe :

```python
def deplacerJoueurX(self, pasX):
    x, y = self.tour.caseX, self.tour.caseY
    if not self.graphe.has_edge((y, x), (y, x + pasX)):
        return False
    return self.tour.deplacerX(pasX)
```

Un déplacement est impossible si l'arête a été supprimée par une barrière. Le graphe est la **source de vérité** pour la légalité des mouvements.

---

### Dijkstra pour le plus court chemin

L'algorithme de Dijkstra (via NetworkX) est utilisé à deux niveaux :

**1. Vérification de chemin possible**
```python
def dijkstra(self, case1, case2):
    try:
        return shortest_path_length(self.graphe, case1, case2)
    except NetworkXNoPath:
        return -1
```

**2. Navigation du bot**
```python
chemin = dijkstra_path(self.graphe, posJoueur, (ligne_arrivee, k))
```

Le bot calcule le chemin optimal vers chacune des 9 cases de sa ligne d'arrivée, et retient le plus court.

---

### Intelligence artificielle basée sur les graphes

Le bot évalue **toutes les positions de barrières possibles** (8×8 horizontales + 8×8 verticales = 128 barrières testées) en calculant pour chacune un **score différentiel** :

```
score = longueur_chemin_ennemi - longueur_chemin_bot
```

Chaque test implique :
1. Modifier le graphe (poser la barrière)
2. Lancer Dijkstra pour le bot et l'ennemi
3. Calculer le score
4. Restaurer le graphe (retirer la barrière)

C'est une **exploration exhaustive de l'espace des états du graphe**, ce qui illustre directement l'intérêt de la modélisation par graphe : modifier et interroger la structure de manière dynamique.

---

## Structure du projet

```
Quoridor/
├── logique.py      # Modèle : graphe, joueurs, barrières, Dijkstra, bot
├── affichage.py    # Vue : interface Tkinter
└── main.py         # Point d'entrée
```

## Dépendances

```bash
pip install networkx matplotlib
```

## Lancement

```bash
python3 main.py
```

---

## Récapitulatif des opérations graphe utilisées

| Opération | Usage dans le projet |
|---|---|
| `add_node` | Initialisation de la grille |
| `add_edge` | Connexion des cases / restauration de barrière |
| `remove_edge` | Pose d'une barrière |
| `has_edge` | Validation d'un déplacement |
| `shortest_path_length` | Vérification de chemin possible |
| `shortest_path` (Dijkstra) | Navigation du bot, évaluation des barrières |
