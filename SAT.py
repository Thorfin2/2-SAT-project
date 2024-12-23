#-----------------------------------------------Exo1&2---------------------------------------------#

#voir Rapport

#------------------------------------------------Exo3----------------------------------------------#

"""
    Convertit un chiffre entre 1 et 26 en la lettre correspondante (a-z).

    Paramètre :
        indice (int) : Entier entre 1 et 26.

    Retourne :
        String : Lettre correspondante à l'indice (a pour 1, z pour 26).
"""
def convertir_en_lettre(indice):
    
    if 1 <= indice <= 26:
        return chr(indice + 96)
    
    

"""
    Transforme une liste 2D représentant une formule 2-SAT en une chaîne lisible sous forme de formule logique.

    Paramètre :
        liste_2d (liste) : Liste 2D où chaque sous-liste représente une clause (ex : [[1, 2], [1, -2]]).

    Retourne :
        String : Formule SAT sous forme de chaîne (ex : "(a|b)&(a|!b)").
"""
def transformer_en_formule_sat(liste_2d):
    formule = ""
    for clause in liste_2d:
        formule += "("
        for index, literal in enumerate(clause):
            if literal > 0:
                formule += convertir_en_lettre(literal)
            else:
                formule += "!"
                formule += convertir_en_lettre(abs(literal))

            # Ajouter un '|' entre les littéraux sauf pour le dernier de la clause
            if index < len(clause) - 1:
                formule += "|"
        formule += ")"

        # Ajouter '&' entre les clauses sauf pour la dernière
        if clause != liste_2d[-1]:
            formule += "&"

    return formule

"""
    Trouve la plus grande variable dans une formule 2-SAT.

    Paramètre :
        formule (liste) : Liste de clauses représentant une formule 2-SAT.

    Retourne :
        int : Plus grande valeur absolue parmi les littéraux.
"""
def trouver_max(formule):
    maximum = 0
    for clause in formule:
        grand = max(clause)
        petit = abs(min(clause))
        if grand > maximum:
            maximum = grand
        if petit > maximum:
            maximum = petit
    return maximum


"""
    Vérifie si la formule est bien formée et si toutes les variables ont une valeur attribuée.

    Paramètres :
        formule (liste) : Liste de clauses représentant une formule 2-SAT.
        valeurs (liste) : Liste des valeurs attribuées aux littéraux.

    Retourne :
        bool : True si la formule est correcte et toutes les variables ont une valeur, False sinon.
"""
def verifier_formule(formule, valeurs):
    if trouver_max(formule) >= len(valeurs):
        print("Vous n'avez pas attribué de valeur à toutes les variables.")
        return False

    for clause in formule:
        for littéral in clause:
            if littéral > 0:
                if valeurs[littéral] not in [0, 1]:
                    print("Les variables doivent avoir des valeurs de 0 ou 1.")
                    return False

    return True



"""
    Vérifie si une formule 2-SAT est satisfiable avec les valeurs données.

    Paramètres :
        formule (liste) : Liste de clauses représentant une formule 2-SAT (chaque clause est une liste de deux littéraux).
        valeurs (liste) : Liste des valeurs attribuées à chaque littéral (1 pour True, 0 pour False).

    Retourne :
        bool : True si la formule est satisfiable, False sinon.
"""
def verifier_sat(formule, valeurs):
    if not verifier_formule(formule, valeurs):
        print("La formule est incorrecte.")
        return formule, valeurs

    resultat_global = True
    temporaire = []
    resultat_clause = True

    for clause in formule:
        for littéral in clause:
            if littéral > 0:
                temporaire.append(valeurs[littéral])
            else:
                temporaire.append(abs(valeurs[abs(littéral)] - 1))

        for i in range(len(temporaire)):
            if i == 0:
                resultat_clause = temporaire[i]
            else:
                resultat_clause = resultat_clause or temporaire[i]

        temporaire.clear()
        resultat_global = resultat_global and resultat_clause

    return resultat_global





#------------------------------------------------Exo4----------------------------------------------#

"""
    Convertit une formule 2-SAT en un graphe orienté.
    Chaque clause est transformée en deux arêtes selon les implications logiques.

    Paramètre :
        formule (liste) : Liste de clauses, chaque clause contenant deux littéraux.

    Retourne :
        graphe (DiGraph) : Graphe orienté correspondant à la formule.
"""
def convertir_formule_en_graphe(formule):
    aretes = []
    for clause in formule:
        aretes.append([-clause[0], clause[1]])  # -a -> b
        aretes.append([-clause[1], clause[0]])  # -b -> a

    graphe = DiGraph()
    graphe.add_edges(aretes)
    return graphe
    
#------------------------------------------------Exo5----------------------------------------------#


# Liste pour stocker les composantes fortement connexes
global_partition = []



"""
'convertir_sommets_positifs' : Fonction qui convertit les sommets négatifs en positifs.
Paramètres:
- graphe_source : Graphe contenant des sommets (présence possible de signes négatifs).
- graphe_cible : Graphe où les sommets seront uniquement positifs.
Fonctionnalité : Copier les arêtes du graphe_source dans le graphe_cible tout en changeant les sommets négatifs en positifs.
Sortie: void (rien).
"""
def convertir_sommets_positifs(graphe_source, graphe_cible):
    sommets_convertis = []
    for i in range(len(graphe_source.edges())):
        sommet_depart = graphe_source.edges()[i][0]
        sommet_arrivee = graphe_source.edges()[i][1]
        sommets_convertis.append([sommet_depart, sommet_arrivee])
    
    min_valeur = 0
    for arete in sommets_convertis:
        minimum = min(arete)
        if min_valeur > minimum:
            min_valeur = minimum
    
    for i in range(len(sommets_convertis)):
        for j in range(len(sommets_convertis[i])):
            sommets_convertis[i][j] += abs(min_valeur)
    
    graphe_cible.add_edges(sommets_convertis)

    
    
"""
    Ajuste les sommets des composantes fortement connexes (CFC) pour correspondre aux valeurs d'origine du graphe principal.
    
    Paramètres:
    - cfc_ensemble : Liste des composantes fortement connexes.
    - graphe_principal : Graphe avec les sommets d'origine (valeurs négatives possibles).
"""
def ajuster_cfc(cfc_ensemble, graphe_principal):
    sommets_graphe = []
    for i in range(len(graphe_principal.edges())):
        sommet_depart = graphe_principal.edges()[i][0]
        sommet_arrivee = graphe_principal.edges()[i][1]
        sommets_graphe.append([sommet_depart, sommet_arrivee])
    
    valeur_min = 0
    for arete in sommets_graphe:
        minimum = min(arete)
        if valeur_min > minimum:
            valeur_min = minimum
    
    for i in range(len(cfc_ensemble)):
        for j in range(len(cfc_ensemble[i])):
            cfc_ensemble[i][j] += valeur_min
    
    # Supprime l'ensemble inutile obtenu après la conversion
    if [0] in cfc_ensemble:
        cfc_ensemble.remove([0])
        
        
        
        
"""
    Explore les sommets du graphe pour détecter les composantes fortement connexes (CFC) à l'aide de l'algorithme de Tarjan.

    Paramètres :
        sommet (int) : Le sommet en cours d'exploration.
        num (int) : Le numéro d'ordre de découverte.
        numero (liste) : Liste contenant l'ordre de découverte des sommets.
        numAccessible (liste) : Liste contenant les plus petits numéros accessibles pour chaque sommet.
        pile (liste) : Pile utilisée pour stocker les sommets en cours d'exploration.
        graphe (DiGraph) : Graphe orienté à explorer.

    Retourne :
        None : Ajoute directement les composantes fortement connexes à la variable globale `partition`.
"""
def parcours(sommet, num, numero, numAccessible, pile, graphe):
    if sommet < 0 or sommet >= len(numero):
        return
    numero[sommet] = num
    numAccessible[sommet] = num
    num += 1
    pile.append(sommet)
    composante = []
    global partition

    for edge in graphe.edges():
        if sommet == edge[0]:
            successeur = edge[1]
            if 0 <= successeur < len(numero) and numero[successeur] is None:
                parcours(successeur, num, numero, numAccessible, pile, graphe)
                numAccessible[sommet] = min(numAccessible[sommet], numAccessible[successeur])
            elif successeur in pile:
                numAccessible[sommet] = min(numAccessible[sommet], numero[successeur])

    if numAccessible[sommet] == numero[sommet]:
        while True:
            sommet_retire = pile.pop()
            composante.append(sommet_retire)
            if sommet_retire == sommet:
                break
        partition.append(composante)


"""
    Implémente l'algorithme de Tarjan pour trouver les composantes fortement connexes.

    Paramètre :
        graphe (DiGraph) : Graphe orienté.

    Retourne :
        liste_cfc (liste) : Liste des composantes fortement connexes.
"""
def tarjan(graphe):
    num = 0
    pile = []
    global partition
    partition = []
    nb_sommets = max(max(abs(edge[0]), abs(edge[1])) for edge in graphe.edges()) + 1
    numero = [None] * nb_sommets
    numAccessible = [None] * nb_sommets
    composantes = []

    for sommet in range(nb_sommets):
        if numero[sommet] is None:
            parcours(sommet, num, numero, numAccessible, pile, graphe)

    for composante in partition:
        if composante:
            composantes.append(composante)

    return composantes


"""
    Vérifie si une formule 2-SAT est satisfiable à partir des composantes fortement connexes.

    Paramètre :
        cfc (liste) : Liste des composantes fortement connexes (CFC).

    Retourne :
        bool : True si la formule est satisfiable, False sinon.
"""
def est_satisfiable(cfc):
    
    for composante in cfc:
        # Convertit la liste en ensemble pour vérifier les doublons (opposés dans la même CFC).
        composante_set = set(composante)
        if len(composante) != len(composante_set):
            return False
    return True


"""
    Associe des valeurs (True ou False) aux littéraux en fonction des composantes fortement connexes (CFC).

    Paramètre :
        cfc (liste) : Liste des composantes fortement connexes.

    Retourne :
        liste : Liste des valeurs assignées à chaque littéral (1 pour True, 0 pour False).
"""
def attribuer_valeurs(cfc):
    
    valeurs = []
    pile_verification = []

    # Initialisation des valeurs des littéraux
    for _ in range(10):  # Taille arbitraire
        valeurs.append(None)

    resultat = []

    # Attribution des valeurs en parcourant les composantes
    for composante in cfc:
        for sommet in composante:
            if abs(sommet) not in pile_verification:
                if sommet > 0:
                    valeurs[sommet] = 1
                else:
                    valeurs[abs(sommet)] = 0
                pile_verification.append(abs(sommet))

    # Préparation du résultat
    for index, valeur in enumerate(valeurs):
        if index == 0:
            resultat.append(None)  # Ignorer l'indice 0
        elif valeur is not None:
            resultat.append(valeur)

    return resultat




"""
    Teste le fonctionnement complet de la vérification de satisfiabilité pour une formule 2-SAT (exo5).
    
    Retourne :
        int : 1 si la formule est satisfiable, 0 sinon.
"""
def tester_exo5():
    graphe_initial = DiGraph()
    graphe_positif = DiGraph()
    formule = [[1, 2], [2, -3], [-2, -4], [2, 4], [4, 1]]

    # Transformer la formule en graphe
    graphe_initial = convertir_formule_en_graphe(formule)
    graphe_initial.show()

    # Copier le graphe en changeant les sommets en positifs
    convertir_sommets_positifs(graphe_initial, graphe_positif)

    # Trouver les composantes fortement connexes
    cfc = tarjan(graphe_positif)

    # Ajuster les composantes avec les sommets originaux (positifs et négatifs)
    ajuster_cfc(cfc, graphe_initial)

    if est_satisfiable(cfc):
        # Affecter des valeurs en fonction de l'ordre topologique inverse
        valeurs = attribuer_valeurs(cfc)
        print("Formule :", transformer_en_formule_sat(formule))
        print("Valeurs :", valeurs)
        print("Résultat de verification de la satisfiabilité :")
        return verifier_sat(formule, valeurs)

    print("La formule n'est pas satisfiable.")
    return 0


#fonction main pour l'executions des differents exercices :
if __name__ == "__main__":
    print( "\n---------------------------------------------exo3---------------------------------------------")
    formule = [[1, 2], [-1, -2]]
    valeur = [None, 1, 0]  # None pour l'indice 0 car les variables commencent à 1

    print("Formule SAT :", transformer_en_formule_sat(formule))
    resultat = verifier_sat(formule, valeur)
    print("Résultat de l'évaluation :", resultat)
    
    print( "\n---------------------------------------------exo4---------------------------------------------")
    
    
    print( "le graphe orienté associé à la formule 2-SAT Donnée")
    formule2 = [[1, 2], [2, -3], [-2, -4], [2, 4], [4, 1]]

    # Convertir la formule en graphe
    graph =convertir_formule_en_graphe(formule2)


    # Afficher le graphe
    graph.show()
    print( "\n---------------------------------------------exo5---------------------------------------------")
    print(tester_exo5())


