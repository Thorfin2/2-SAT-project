from graphviz import Digraph

"""
    Convertit une formule 2-SAT en un graphe orienté.

    Arguments :
        formule : liste 2D, chaque sous-liste représente une clause [a, b].

    Retourne :
        Un graphe orienté où chaque clause (a ∨ b) est convertie en :
        . -a → b
        . -b → a
    """
def towSatToGraph(formule):
    edges = []

    for clause in formule:
        if len(clause) != 2:
            raise ValueError("Chaque clause doit contenir exactement 2 littéraux.")

        # Ajouter les implications basées sur la clause
        edges.append((-clause[0], clause[1]))  # -a → b
        edges.append((-clause[1], clause[0]))  # -b → a

    # Créer un graphe orienté
    graph = Digraph()
    for edge in edges:
        graph.edge(f"x{abs(edge[0])}" + ("'" if edge[0] < 0 else ""),
                   f"x{abs(edge[1])}" + ("'" if edge[1] < 0 else ""))

    return graph, edges

# Exemple d'utilisation
if __name__ == "__main__":
    formule = [[1, 2], [2, -3], [-2, -4], [2, 4], [4, 1]]

    # Convertir la formule en graphe
    graph, edges = towSatToGraph(formule)

    # Afficher les arêtes pour vérification
    print("Le graphe contient les arêtes suivantes :")
    for edge in edges:
        print(f"{edge[0]} -> {edge[1]}")

    # Sauvegarder et afficher le graphe
    graph.render("graph_2SAT", format="png", cleanup=True)
    print("Le graphe a été rendu dans le fichier 'graph_2SAT.png'.")
