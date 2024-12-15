partition = []
def towSatToGraph(formul):
    tmp = []
    for l in formul:
        tmp.append([l[0]*-1,l[1]])
        tmp.append([l[1]*-1,l[0]])
    g = DiGraph()
    g.add_edges(tmp)
    return g



"""
'changeToPositif ': fonction qui change les signes des des sommets de ( - ) à ( + )
Paramètres:
- g : Graphe avec des sommets ( presence de signes negatifs possible)
- f : Graphe ( eliminations des signes negatifs )
Fonctionalité  : copier le premier graphe g  (qui a des valeurs negatifs pour les sommets) dans le deuxieme graphe f 
on va utiliser cette fonction  pour l'algo de tarjan qui fonctionne avec des sommets positifs 
Sortie: void ( rien ) 
"""
def changeToPositif (g,f):
    ch = []
    for i in range(len(g.edges())):
        x = g.edges()[i][0]
        y = g.edges()[i][1]
        ch.append([x,y])
    x = 0
    for i in ch:
        mini = min(i)
        if x > mini:
            x = mini
    for i in range(len(ch)):
        for j in range(len(ch[i])):
            ch[i][j] += abs(x)
    f.add_edges(ch)

#prend l,enseble des cfc et le graph principale(avec les valeur negatifs)
def changeEnsemble (l,g):
    ch = []
    for i in range(len(g.edges())):
        x = g.edges()[i][0]
        y = g.edges()[i][1]
        ch.append([x,y])
    x = 0
    for i in ch:
        mini = min(i)
        if x > mini:
            x = mini
    for i in range(len(l)):
        for j in range(len(l[i])):
            l[i][j] += x
    #avec le convertition que j'ai fait on obtient un ensemble qui n'existe pas
    l.remove([0])
    

def parcours (v,num,numero,numAccessible,pile,gr):
    numero[v] = num
    numAccessible[v] = num
    num += 1
    pile.append(v)
    c = []
    global partition
    for i in range(len(gr.edges())):
        if v == gr.edges()[i][0] :
            w = gr.edges()[i][1] # w est l'arete succeseur de v
            if numero[w] == None:
                parcours(w,num,numero,numAccessible,pile,gr)
                numAccessible[v] = min(numAccessible[v] , numAccessible[w])
            elif w in pile:
                numAccessible[v] = min(numAccessible[v], numero[w])

    if numAccessible[v] == numero[v]:        
        while True:
            w = pile.pop()
            c.append(w)
            if w == v:
                break
    partition.append(c)

def tarjan(gr):
    num = 0
    pile = []
    global partition
    numero = []
    numAccessible = []
    rep = []
    for v in gr:
        numero.append(None)
        numAccessible.append(None)
    numero.append(None)
    numAccessible.append(None)

    for v in range(len(gr.vertices())):
        if numero[v] == None:
            parcours(v,num,numero,numAccessible,pile,gr)
    #boucle pour nous rendre une liste propre(sans listes vide)
    for p in partition:
        if p :
            rep.append(p)
    return rep 

#la formule est satisfable ssi y'a pas un element et ça contrapose dans 
#la meme ensemble de composent fortement connexe
def satisfable (cfc):
    for i in cfc:
        #un set ne contient pas de repetition
        #donc j'ai changé la list en set et j'ai verifié si ils on la meme taille
        a_set = set(i)
        if len(i) != len(a_set):
            return False
    return True

def donnerValeur(cfc):
    valeur = []
    pile_verif = []
    for i in range(10):
        valeur.append(None)
    rep = []
    for i in range(len(cfc)):
        for j in range(len(cfc[i])):
            if abs(cfc[i][j]) not in pile_verif:
                if cfc[i][j] > 0:
                    valeur[cfc[i][j]] = 1
                    pile_verif.append(abs(cfc[i][j]))
                else:
                    valeur[abs(cfc[i][j])] = 0
                    pile_verif.append(abs(cfc[i][j]))
    for i in range(len(valeur)):
        if i == 0:
            rep.append(None)
        if valeur[i] != None:
            rep.append(valeur[i])
    return rep

#prend un chifre entre 1 et 26 et retourne une lettre correspondent
def sommet (s):
    if s > 0 and s < 27:
        return chr(s + 96)

#prend une liste en 2d et la transforme en formule SAT
#ex: [[1,2],[1,-2]] = (a|b)&(a|!b)
def transforme(l):
    str = ""
    for i in range(len(l)):
        str+="("
        for j in range(len(l[i])):
            if l[i][j] > 0:
                str += sommet(l[i][j])
            else:
                str += "!"
                str += sommet(abs(l[i][j]))
            if j < len(l[i]) -1:
                str += "|"

        str+=")"
        if i < len(l)-1:
            str+="&"
    return str

#prend en parametres une formule en format de liste 2d et la list des valeurs 
#1 = true , 0 = false l'indice de la list des valeurs correspond a la valeur
#et ça valeur a la valeur
def SAT (formule, valeur):
    if not isFormul(formule, valeur) :
        print("la formule est incorrect")
        return formule, valeur
    rep = True
    tmp = []
    rep2 = True
    for clause in formule:
        for x in clause:
            if x > 0:
                tmp.append(valeur[x])
            else:
                tmp.append(abs(valeur[abs(x)] -1))
        for T in range(len(tmp)):
            if T == 0:
                rep2 = tmp[T]
            else:
                rep2 = rep2 or tmp[T]
        tmp.clear()
        rep = rep and rep2
    return rep
    
#prend une formule et renvoie le plus grande inconnue
def Max (formule):
    rep = 0
    for clause in formule:
        big = max(clause)
        small = abs(min(clause))
        if big > rep:
            rep = big
        if small > rep:
            rep = small
    return rep
    
#verifie si on a bien formuler la formule et on a attribuer une valeur
#a toutes les variables
def isFormul (formule,valeur):
    if Max(formule) < len(valeur) -1:
        print("vous n'avez pas attribue une valeur a toutes les variables")
        return False
    for clause in formule:
        for x in clause:
            if x > 0:
                if abs(valeur[x]) != 1 and abs(valeur[x]) != 0:
                    print("vous devriez bien attribuer les valeur au variables")
                    return False

    #print("la formule est bien une formule SAT")
    return True

def tester_exo5 ():
    g = DiGraph()
    f = DiGraph()
    formul = [[1,2],[2,-3],[-2,-4],[2,4],[4,1]] #la formule qu'on veut traiter
    #formul = [[1,2],[-1,2],[1,-2]]

    #transformer la formule en graph
    g = towSatToGraph(formul)
    g.show()

    #copier le graph mais changer les valeurs en positifs
    changeToPositif(g,f)

    #stocker les ensembles composente fortement connecté
    cfc = tarjan(f)

    #changer les valeurs de cfc en format initial(positifs et negatifs)
    changeEnsemble(cfc,g)
    if satisfable(cfc):

        #affecter des valeurs (1 ou 0) au attribue en fonction de l'ordre 
        #topologique inverse
        valeur = donnerValeur(cfc)
        print("la formul :", transforme(formul))
        print("pour les valeur", valeur)
        print("a retourner :")
        return SAT(formul,valeur)
    
    print("la formule n'est pas satisfable")
    return 0

print(tester_exo5())


