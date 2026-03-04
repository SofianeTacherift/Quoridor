import tkinter as tk
from logique import *

class FenetreJeu:

    def __init__(self, jeu):
        self.jeu = jeu
        

        self.root = tk.Tk()
        self.root.title("Quoridor")

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Key>", self.on_key)
        self.canvas.bind("<Configure>", self.on_resize)

        self.largeur = 1
        self.hauteur = 1
        self.barriereEnCours=None

        self.root.mainloop()

    def on_resize(self, event):
        self.largeur = event.width
        self.hauteur = event.height
        self.redessiner()

    def on_click(self,event):
        return

        
    def on_key(self, event):

        joueur = self.jeu.tour

        if (joueur==self.jeu.j1): 

            if event.keysym.lower() == "e" and joueur.barrierePosee==False:
                joueur.modeBarriere = not joueur.modeBarriere
                self.barriereEnCours=Barriere((3,2),(3,3),(4,2),(4,3),"horizontal") if joueur.modeBarriere else None
                self.redessiner()
                return

            if joueur.modeBarriere and event.keysym.lower() == "a":
                if self.jeu.poserBarriere(self.barriereEnCours):
                    joueur.modeBarriere=False
                    self.barriereEnCours=None
                    self.redessiner()
                return


            if not joueur.modeBarriere:

                x = joueur.caseX
                y = joueur.caseY

                deplacement=False


                if event.keysym.lower() == "z":
                    deplacement=self.jeu.deplacerJoueurY(-1)



                elif event.keysym.lower() == "s": 
                    deplacement=self.jeu.deplacerJoueurY(1)

                
                elif event.keysym.lower() == "q":
                    deplacement=self.jeu.deplacerJoueurX(-1)

                elif event.keysym.lower() == "d":
                    deplacement=self.jeu.deplacerJoueurX(1)


                if (deplacement):
                    self.jeu.changerJoueur()
                    self.redessiner()
                    self.tourBot()
            
            elif joueur.modeBarriere:
                match (event.keysym.lower()):

                    case "d":
                        self.barriereEnCours.deplacerX(1)

                    case "q":
                        self.barriereEnCours.deplacerX(-1)

                    case "s":
                        self.barriereEnCours.deplacerY(1)

                    case "z":
                        self.barriereEnCours.deplacerY(-1)
                    

                self.redessiner()

    def tourBot(self):
        self.jeu.jouerBot()
        self.redessiner()
            


    def redessiner(self):
        self.canvas.delete("all")
        self.dessiner_grille()
        self.dessiner_barrieres()
        self.dessiner_joueurs()

    def dessiner_grille(self):
        cell_w = self.largeur / 9
        cell_h = self.hauteur / 9

        for i in range(10):
            # verticales
            x = i * cell_w
            self.canvas.create_line(x, 0, x, self.hauteur)

            # horizontales
            y = i * cell_h
            self.canvas.create_line(0, y, self.largeur, y)

    def dessiner_joueurs(self):
        cell_w = self.largeur / 9
        cell_h = self.hauteur / 9

        # Joueur 1
        x = self.jeu.j1.caseX * cell_w + cell_w/2
        y = self.jeu.j1.caseY * cell_h + cell_h/2
        self.canvas.create_oval(x-self.hauteur/18+5, y-self.hauteur/18+5, x+self.hauteur/18-5, y+self.hauteur/18-5, fill="red")

        x = self.jeu.j2.caseX * cell_w + cell_w/2
        y = self.jeu.j2.caseY * cell_h + cell_h/2
        self.canvas.create_oval(x-self.hauteur/18+5, y-self.hauteur/18+5, x+self.hauteur/18-5, y+self.hauteur/18-5, fill="blue")

    def dessiner_barrieres(self):
        cell_w = self.largeur / 9
        cell_h = self.hauteur / 9

        if (self.barriereEnCours):
            if self.barriereEnCours.direction=="horizontal":
                x1 = self.barriereEnCours.NO[1] * cell_w
                y1 = self.barriereEnCours.NO[0] * cell_h + cell_h
                x2 = self.barriereEnCours.NE[1] * cell_w + cell_w
                self.canvas.create_rectangle(x1, y1-5, x2, y1+5, fill="brown")
            else:
                x1 = self.barriereEnCours.NO[1] * cell_w + cell_w
                y1 = self.barriereEnCours.NO[0] * cell_h
                y2 = self.barriereEnCours.SO[0] * cell_h + cell_h
                self.canvas.create_rectangle(x1-5, y1, x1+5, y2, fill="brown")


        for b in self.jeu.listeBarrieres:
            if b.direction=="horizontal":
                x1 = b.NO[1] * cell_w
                y1 = b.NO[0] * cell_h + cell_h
                x2 = b.NE[1] * cell_w + cell_w
                self.canvas.create_rectangle(x1, y1-5, x2, y1+5, fill="brown")
            else:
                x1 = b.NO[1] * cell_w + cell_w
                y1 = b.NO[0] * cell_h
                y2 = b.SO[0] * cell_h + cell_h
                self.canvas.create_rectangle(x1-5, y1, x1+5, y2, fill="brown")
    
