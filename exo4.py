def towSatToGraph(formul):
    tmp = []
    #ça prend aVb et rend (~a->b)(~b->a) et les mets dans une liste
    for l in formul:
        tmp.append([l[0]*-1,l[1]])
        tmp.append([l[1]*-1,l[0]])
    print(tmp)
    g = DiGraph()
    g.add_edges(tmp)
    return g 

g = DiGraph()
l = [[1,2],[2,-3],[-2,-4],[2,4],[4,1]]
g = towSatToGraph(l)
for v in g:
    print(v)
g.show()
