from networkx import *
import pylab as P

class Joueur :
    
    def __init__(self, i, couleur,x,y):
        self.id=i
        self.couleur=couleur
        self.caseX=x
        self.caseY=y
        self.modeBarriere=False
    
    
    def deplacerX(self, x):
        if (self.caseX+x<0 or self.caseX+x>8):
            return False
        else:
            self.caseX+=x 
            return True

    def deplacerY(self, y):
        if (self.caseY+y<0 or self.caseY+y>8):
            return False
        else:
            self.caseY+=y 
            return True
    

class Barriere:

    def __init__(self,t1,t2,t3,t4,direct):
        self.NO=t1
        self.NE=t2
        self.SO=t3
        self.SE=t4
        self.direction=direct
    
    def changerdirection(self):
        if (self.direction=="horizontal"):
            self.direction="vertical"
        elif (self.direction=="vertical"):
            self.direction="horizontal"
    
    def deplacerX(self, x):
        caseAVerifier = self.NO if x < 0 else self.NE
        if (caseAVerifier[0] + x >= 0 and caseAVerifier[0] + x <= 8):
            self.NO = (self.NO[0] + x, self.NO[1])
            self.NE = (self.NE[0] + x, self.NE[1])
            self.SO = (self.SO[0] + x, self.SO[1])
            self.SE = (self.SE[0] + x, self.SE[1])
            return True
        return False

    def deplacerY(self, y):
        caseAVerifier = self.NO if y < 0 else self.SO
        if (caseAVerifier[1] + y >= 0 and caseAVerifier[1] + y <= 8):
            self.NO = (self.NO[0], self.NO[1] + y)
            self.NE = (self.NE[0], self.NE[1] + y)
            self.SO = (self.SO[0], self.SO[1] + y)
            self.SE = (self.SE[0], self.SE[1] + y)
            return True
        return False    

    

class Jeu:



    
    def __init__(self):
        self.j1 = Joueur(0,1,4,8)
        self.j2= Joueur(0,2,4,0)
        self.initGraphe()
        self.listeBarrieres=[]
        self.tour=self.j1

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

    def ajouterArretes(self,n1,n2):
        self.graphe.add_edge(n1,n2)

    def poserBarriere(self,barriere):
        if (barriere.direction=="horizontal"):
            self.casserArretes(barriere.NO,barriere.SO)
            self.casserArretes(barriere.NE,barriere.SE)
        else:
            self.casserArretes(barriere.NO,barriere.NE)
            self.casserArretes(barriere.SO,barriere.SE)         
        self.listeBarrieres.append(barriere)

        if ( not self.cheminPossibleJoueur(self.j1) or not self.cheminPossibleJoueur(self.j2)):
            self.casserBarriere(barriere)
            return False 
        return True

    def casserBarriere(self,barriere):
        if (barriere.direction=="horizontal"):
            self.ajouterArretes(barriere.NO,barriere.SO)
            self.ajouterArretes(barriere.NE,barriere.SE)
        else:
            self.ajouterArretes(barriere.NO,barriere.NE)
            self.ajouterArretes(barriere.SO,barriere.SE) 
        self.listeBarrieres.remove(barriere)
    
    def deplacerJoueurX(self, x):
        return self.tour.deplacerX(x)

    def deplacerJoueurY(self,y):
        return self.tour.deplacerY(y)
        

    



    def dijkstra(self, case1, case2):
        try:
            return shortest_path_length(self.graphe, case1, case2)
        except NetworkXNoPath:
            return -1
    
    def cheminPossibleJoueur(self, joueur):
        i=9 if joueur==self.j2 else 0
        for j in range(9):
            if (self.dijkstra((joueur.caseY, joueur.caseX),(i,j))!=-1):
                return True 
        return False
    

            




    
    def changerJoueur(self):
        self.tour=self.j2 if self.tour==self.j1 else self.j1
    

    

     
    

    
     
    







        


        