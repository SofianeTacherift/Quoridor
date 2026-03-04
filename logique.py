from networkx import *
import pylab as P

class Joueur :
    
    def __init__(self, i, couleur,x,y):
        self.id=i
        self.couleur=couleur
        self.caseX=x
        self.caseY=y
        self.modeBarriere=False
        self.barrierePosee=False
    
    
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
        if (caseAVerifier[1] + x >= 0 and caseAVerifier[1] + x <= 8):
            self.NO = (self.NO[0], self.NO[1] + x)
            self.NE = (self.NE[0], self.NE[1] + x)
            self.SO = (self.SO[0], self.SO[1] + x)
            self.SE = (self.SE[0], self.SE[1] + x)
            return True
        return False

    def deplacerY(self, y):
        caseAVerifier = self.NO if y < 0 else self.SO
        if (caseAVerifier[0] + y >= 0 and caseAVerifier[0] + y <= 8):
            self.NO = (self.NO[0] + y, self.NO[1])
            self.NE = (self.NE[0] + y, self.NE[1])
            self.SO = (self.SO[0] + y, self.SO[1])
            self.SE = (self.SE[0] + y, self.SE[1])
            return True
        return False  



    

class Jeu:



    
    def __init__(self):
        self.j1 = Joueur(0,1,4,8)
        self.j2= Joueur(0,2,4,0)
        self.initGraphe()
        self.listeBarrieres=[]
        self.tour=self.j1
        self.gagnant=None

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
        if not (self.graphe.has_edge(n1,n2)): return False
        self.graphe.remove_edge(n1,n2)
        return True

    def ajouterArretes(self,n1,n2):
        self.graphe.add_edge(n1,n2)

    def poserBarriere(self,barriere):

        if (barriere.direction=="horizontal"):
            res = self.casserArretes(barriere.NO,barriere.SO) and self.casserArretes(barriere.NE,barriere.SE)
        else:
            res = self.casserArretes(barriere.NO,barriere.NE) and self.casserArretes(barriere.SO,barriere.SE)

        if not res: return res
        self.listeBarrieres.append(barriere)
    
        if ( not self.cheminPossibleJoueur(self.j1) or not self.cheminPossibleJoueur(self.j2)):
            self.casserBarriere(barriere)
            self.tour.barrierePosee=False
            return False 
        self.tour.barrierePosee=True
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
        i=8 if joueur==self.j1 else 0
        for j in range(9):
            if (self.dijkstra((joueur.caseY, joueur.caseX),(i,j))!=-1):
                return True 
        return False
    

    def changerJoueur(self):
        self.tour=self.j2 if self.tour==self.j1 else self.j1
        self.tour.barrierePosee=False


    def testerBarriere(self, barriere):
        posJoueur = (self.j2.caseY, self.j2.caseX)
        posEnnemi = (self.j1.caseY, self.j1.caseX)
        iJoueur = 0  
        iEnnemi = 8  

        if self.poserBarriere(barriere):

            meilleurCheminJoueur = None
            for k in range(9):
                try:
                    chemin = dijkstra_path(self.graphe, posJoueur, (iEnnemi, k))
                    if meilleurCheminJoueur is None or len(chemin) < len(meilleurCheminJoueur):
                        meilleurCheminJoueur = chemin
                except NetworkXNoPath:
                    continue

            meilleurCheminEnnemi = None
            for k in range(9):
                try:
                    chemin = dijkstra_path(self.graphe, posEnnemi, (iJoueur, k))
                    if meilleurCheminEnnemi is None or len(chemin) < len(meilleurCheminEnnemi):
                        meilleurCheminEnnemi = chemin
                except NetworkXNoPath:
                    continue

            self.casserBarriere(barriere)

            if meilleurCheminJoueur and meilleurCheminEnnemi:
                score = len(meilleurCheminEnnemi) - len(meilleurCheminJoueur)
                return meilleurCheminJoueur, score

        return None, float("-inf")

                    


        

    def meilleureBarriereBot(self):
        meilleureBarriere=None
        for i in range(8):
            for j in range(8):
                print((i,j),(i,j+1),(i+1,j),(i+1, j+1) )
                NO=(i,j)
                NE=(i,j+1)
                SO=(i+1,j)
                SE=(i+1,j+1)

                barriereHorizontale=Barriere(NO,NE,SO,SE,"horizontal")
                cheminEtScore=self.testerBarriere(barriereHorizontale)
                chemin=cheminEtScore[0]
                score=cheminEtScore[1]
                if (chemin is None): continue

                if (meilleureBarriere is None) or (score>meilleureBarriere[2]):

                    meilleureBarriere=(barriereHorizontale,chemin,score)
        return meilleureBarriere


    def jouerBot(self):
        if not self.tour==self.j2: return 

        meilleureBarriere,chemin,score=self.meilleureBarriereBot()
        print(meilleureBarriere, chemin)
        self.poserBarriere(meilleureBarriere)
        prochaineCase=chemin[1]
        diffX=prochaineCase[1]-self.j2.caseX
        diffY=prochaineCase[0]-self.j2.caseY
        if (diffX!=0):
            self.deplacerJoueurX(diffX)
        elif diffY!=0:
            self.deplacerJoueurY(diffY)
        self.changerJoueur()
    


    











    

    

     
    

    
     
    







        


        