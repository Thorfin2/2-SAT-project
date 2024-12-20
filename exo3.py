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


formul = [[1,2],[-1,-2]]
valeur = [None,1,0]
print("la formule est: " + transforme(formul) + " et ça valeur est:")
print(SAT(formul,valeur))
