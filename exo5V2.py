# Liste pour stocker les composantes fortement connexes
global_partition = []

"""
    Convertit une formule 2-SAT en un graphe orienté.
    Chaque clause est transformée en deux arêtes selon les implications logiques.

    Paramètre :
        formule (list) : Liste de clauses, chaque clause contenant deux littéraux.

    Retourne :
        graphe (Digraph) : Graphe orienté correspondant à la formule.
"""
def convertir_formule_en_graphe(formule):
    aretes = []
    for clause in formule:
        aretes.append([-clause[0], clause[1]])  # ¬a -> b
        aretes.append([-clause[1], clause[0]])  # ¬b -> a

    graphe = Digraph()
    graphe.edges(aretes)
    return graphe

"""
    Convertit les sommets d'un graphe initial en valeurs positives et les copie dans un graphe final.

    Paramètres :
        graphe_initial (Digraph) : Graphe contenant des sommets négatifs.
        graphe_final (Digraph) : Graphe où les sommets seront positifs.
"""
def convertir_sommets_positifs(graphe_initial, graphe_final):
    aretes_converties = []
    for edge in graphe_initial.edges():
        aretes_converties.append([abs(edge[0]), abs(edge[1])])

    graphe_final.edges(aretes_converties)
    
    
"""
    Ajuste les sommets des CFC pour correspondre aux valeurs originales (positives et négatives).

    Paramètres :
        cfc (list) : Liste des composantes fortement connexes.
        graphe_initial (Digraph) : Graphe avec des sommets originaux.
"""
def ajuster_ensemble_cfc(cfc, graphe_initial):
    decalage = min(min(edge) for edge in graphe_initial.edges())
    for composante in cfc:
        for i in range(len(composante)):
            composante[i] -= abs(decalage)

    if [0] in cfc:
        cfc.remove([0])


"""
    Implémente l'algorithme de Tarjan pour trouver les composantes fortement connexes.

    Paramètre :
        graphe (Digraph) : Graphe orienté.

    Retourne :
        liste_cfc (list) : Liste des composantes fortement connexes.
"""
def algorithme_tarjan(graphe):
    global global_partition
    global_partition.clear()
    num = 0
    pile = []
    numero = {v: None for v in graphe.nodes()}
    num_accessible = {v: None for v in graphe.nodes()}

    def parcours(v):
        nonlocal num
        numero[v] = num
        num_accessible[v] = num
        num += 1
        pile.append(v)
        composante = []

        for successeur in graphe.successors(v):
            if numero[successeur] is None:
                parcours(successeur)
                num_accessible[v] = min(num_accessible[v], num_accessible[successeur])
            elif successeur in pile:
                num_accessible[v] = min(num_accessible[v], numero[successeur])

        if num_accessible[v] == numero[v]:
            while True:
                w = pile.pop()
                composante.append(w)
                if w == v:
                    break
            global_partition.append(composante)

    for sommet in graphe.nodes():
        if numero[sommet] is None:
            parcours(sommet)

    return [c for c in global_partition if c]

"""
    Vérifie si la formule est satisfiable à partir des composantes fortement connexes.

    Paramètre :
        cfc (list) : Liste des composantes fortement connexes.

    Retourne :
        bool : True si la formule est satisfiable, False sinon.
"""
def verifier_satisfiabilite(cfc):
    for composante in cfc:
        ensemble = set(composante)
        for sommet in composante:
            if -sommet in ensemble:
                return False
    return True


"""
    Associe des valeurs (True ou False) aux littéraux en fonction des CFC.

    Paramètre :
        cfc (list) : Liste des composantes fortement connexes.

    Retourne :
        valeurs (dict) : Dictionnaire associant chaque littéral à sa valeur.
"""
def attribuer_valeurs(cfc):
    valeurs = {}
    traites = set()

    for composante in cfc:
        for sommet in composante:
            if sommet not in traites:
                valeurs[abs(sommet)] = sommet > 0
                traites.add(abs(sommet))

    return valeurs


"""
    Teste l'ensemble du processus pour vérifier une formule 2-SAT.
"""
def tester_exo5():
    formule = [[1, 2], [2, -3], [-2, -4], [2, 4], [4, 1]]
    graphe = convertir_formule_en_graphe(formule)

    graphe_pos = Digraph()
    convertir_sommets_positifs(graphe, graphe_pos)

    cfc = algorithme_tarjan(graphe_pos)
    ajuster_ensemble_cfc(cfc, graphe)

    if verifier_satisfiabilite(cfc):
        valeurs = attribuer_valeurs(cfc)
        print("Formule satisfiable avec les valeurs :", valeurs)
    else:
        print("La formule n'est pas satisfiable.")

tester_exo5()
