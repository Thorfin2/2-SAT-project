def sommet(s):
    """
    Convertit un entier en une lettre correspondante (a-z).
    """
    if 1 <= s <= 26:
        return chr(s + 96)
    raise ValueError("Le sommet doit être entre 1 et 26.")

def transforme(formule):
    """
    Transforme une formule sous forme de liste 2D en une représentation textuelle de 2-SAT.
    """
    clauses = []
    for clause in formule:
        literals = []
        for literal in clause:
            if literal > 0:
                literals.append(sommet(literal))
            else:
                literals.append(f"!{sommet(abs(literal))}")
        clauses.append(f"({' | '.join(literals)})")
    return " & ".join(clauses)

def SAT(formule, valeur):
    """
    Évalue si une formule 2-SAT est vraie ou fausse pour une assignation donnée.
    Arguments :
        formule : liste 2D représentant les clauses.
        valeur : liste des valeurs assignées (1 pour vrai, 0 pour faux).
    Retourne :
        True si la formule est vraie, sinon False.
    """
    if not isFormul(formule, valeur):
        return False

    for clause in formule:
        clause_evaluated = False
        for literal in clause:
            if literal > 0:
                clause_evaluated |= bool(valeur[literal])
            else:
                clause_evaluated |= not bool(valeur[abs(literal)])
        if not clause_evaluated:
            return False

    return True

def Max(formule):
    """
    Trouve la plus grande variable utilisée dans la formule.
    """
    return max(abs(literal) for clause in formule for literal in clause)

def isFormul(formule, valeur):
    """
    Vérifie si la formule et l'assignation sont valides.
    """
    max_var = Max(formule)
    if max_var >= len(valeur):
        print("Vous n'avez pas attribué une valeur à toutes les variables.")
        return False

    for val in valeur[1:]:
        if val not in (0, 1):
            print("Les valeurs doivent être 0 ou 1.")
            return False

    return True

# Exemple d'utilisation
if __name__ == "__main__":
    formule = [[1, 2], [-1, -2]]
    valeur = [None, 1, 0]  # None pour l'indice 0 car les variables commencent à 1

    print("Formule SAT :", transforme(formule))
    resultat = SAT(formule, valeur)
    print("Résultat de l'évaluation :", resultat)
