# 2-SAT-project
L3 info : 
NADER Fadi   |
LETAIEF Ahmed Yahya  |
ZNATA Mehdi

Sujet :
[TP-final.pdf](https://github.com/user-attachments/files/18141691/TP-final-2020.pdf)

Questions:

Exercice 1: Soit F une formule 2−Sat avec n variables. Quel est le nombre maximum de clauses que peut comporter F ?

Exercice 2: Donnez un exemple de formule 2−Sat qui n’est pas satisfaisable.

Exercice 3: Ecrivez une fonction qui étant donné une aﬀectation pour les variables déterminé si la formule est évaluée à vrai ou faux.

Exercice 4: Etant donné une formule 2−Sat, écrivez une fonction qui construit le graphe orienté associé.

Exercice 5: A partir du graphe construit à l’exercice précédent , implémentez l’algorithme de [1] qui détermine si la formule est valide ou pas. Si la formule
est valide, la fonction renverra une aﬀectation.


# Projet : Résolution du problème 2-SAT

Ce projet implémente des solutions pour traiter des formules booléennes sous forme de 2-SAT (2-Satisfiability). Le code fournit des fonctionnalités pour vérifier la satisfiabilité d'une formule, construire le graphe orienté associé et déterminer une affectation valide si la formule est satisfiable. Le tout est exécuté sur la plateforme : [SageMath Cell](https://sagecell.sagemath.org/).

## Introduction

Le problème 2-SAT est une sous-classe du problème SAT, où chaque clause est une disjonction de deux littéraux. L'objectif est de déterminer si la formule est satisfiable, c'est-à-dire si une assignation des variables rend la formule vraie. 

Ce projet repose sur les concepts suivants :
- **Formules booléennes** : Exprimées en conjonctive normale (CNF).
- **Graphes orientés** : Représentation des implications logiques des littéraux.
- **Algorithme de Tarjan** : Utilisé pour trouver les composantes fortement connexes (CFC).

---

## Fonctionnalités principales

### 1. Vérification de la satisfiabilité d'une formule (Exercice 3)

La fonction principale de cette section est :

```python
def verifier_sat(formule, valeurs):
```
Cette fonction :
- Vérifie si une formule 2-SAT est correcte et bien formée.
- Évalue chaque clause de la formule en fonction des valeurs des littéraux.
- Retourne `True` si toutes les clauses sont satisfaites, sinon `False`.

Exemple d'entrée :
```python
formule = [[1, 2], [-1, -2]]
valeurs = [None, 1, 0]  # None pour l'indice 0
```
Sortie :
```plaintext
True
```

---

### 2. Construction du graphe orienté (Exercice 4)

La fonction principale ici est :

```python
def convertir_formule_en_graphe(formule):
```
Elle :
- Transforme chaque clause de la formule en deux arêtes orientées.
- Construit un graphe orienté représentant les implications logiques des littéraux.

Exemple d'entrée :
```python
formule = [[1, 2], [-2, -3]]
```
Sortie :
- Un graphe orienté (affichable sur SageMath Cell).

---

### 3. Algorithme de Tarjan et détermination de la satisfiabilité (Exercice 5)

Les fonctions clés incluent :

#### a) Algorithme de Tarjan
```python
def tarjan(graphe):
```
Cette fonction identifie les composantes fortement connexes (CFC) dans un graphe orienté. Les CFC sont cruciales pour vérifier si une formule est satisfiable.

#### b) Vérification de la satisfiabilité
```python
def est_satisfiable(cfc):
```
Elle vérifie si un littéral et sa négation apparaissent dans la même CFC. Si oui, la formule est insatisfiable.

#### c) Attribution des valeurs
```python
def attribuer_valeurs(cfc):
```
Cette fonction :
- Parcourt les CFC dans l'ordre topologique inverse.
- Attribue des valeurs (`1` ou `0`) aux littéraux pour satisfaire la formule.

---

## Exemple complet d'exécution

1. **Formule donnée** :
```python
formule = [[1, 2], [2, -3], [-2, -4], [2, 4], [4, 1]]
```
2. **Étapes exécutées** :
   - Transformation en graphe : `convertir_formule_en_graphe`.
   - Trouver les CFC : `tarjan`.
   - Vérification de la satisfiabilité : `est_satisfiable`.
   - Attribution des valeurs : `attribuer_valeurs`.
3. **Résultat attendu** :
```plaintext
Formule satisfiable avec les valeurs : [None, 1, 0, 1, 0]
```

---


## Remarques
- Les Réponses pour les 2 premiers exercices sont dans le Rapport:  
[Rapport.pdf](Rapport.pdf)
- L'execution du Fichier  SAT.PY se fera sur Sage Math comme mentionné si dessus.
