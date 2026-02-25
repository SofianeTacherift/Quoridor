from networkx import *
import pylab as P

class Joueur :
    
    def __init__(self, i, couleur,x,y):
        self.id=i
        self.couleur=couleur
        self.caseX=x
        self.caseY=y
        self.modeBarriere=False

class Barriere:

    def __init__(self,t1,t2,t3,t4,horizontal):
        self.NO=t1
        self.NE=t2
        self.SO=t3
        self.SE=t4
        self.horizontal=horizontal

    

class Jeu:



    
    def __init__(self):
        self.j1 = Joueur(0,1,4,8)
        self.j2= Joueur(0,2,4,0)
        self.initGraphe()
        self.listeBarrieres=[]
        self.tour="j1"

    def initGraphe(self):
        g=Graph()
        for i in range(9):
            for j in range(9):
                g.add_node((i,j))
                if (i>0):
                    g.add_edge((i,j), (i-1,j))
                if (j>0):
                    g.add_edge((i,j), (i,j-1))
        self.graphe = g

    def casserArretes(self,n1, n2):
        self.graphe.remove_edge(n1,n2)

    def poserBarriere(self,t1,t2,t3,t4,horizontal):
        if (horizontal):
            self.casserArretes(t1,t3)
            self.casserArretes(t2,t4)
        else:
            self.casserArretes(t1,t2)
            self.casserArretes(t3,t4) 
        barriere = Barriere(t1,t2,t3,t4,horizontal)
        self.listeBarrieres.append(barriere)



    def dijikstra(self,case1, case2):
        distance = shortest_path_length(self.graphe, source=case1, target=case2)
        return distance
    

    
     
    







        


        